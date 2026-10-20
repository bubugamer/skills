#!/usr/bin/env python3
"""Build a local review page from actual task or trigger records."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import sys
from task_results import summarize


def escape(value):
    return html.escape(str(value), quote=True)


def render(data, candidate='candidate', baseline='baseline'):
    if not isinstance(data, dict):
        raise ValueError('results must be an object')
    if data.get('kind') == 'task-comparison':
        summary = summarize(data, candidate, baseline)
        rows = data['runs']
        cards = []
        for index, row in enumerate(rows):
            variant = {'candidate': '候选版本', 'baseline': '基准版本'}.get(row['variant'], row['variant'])
            label = f"{row['case_id']} · {variant} · {row['run_id']}"
            details = '\n'.join(f"{'通过' if e['passed'] else '未通过'}：{e['text']}\n依据：{e['evidence']}" for e in row.get('expectations', []))
            cards.append((label, row['status'], row.get('prompt', ''), row.get('output', ''), details or row.get('error', '')))
    elif data.get('kind') == 'trigger-probe':
        rows = data.get('results')
        if not isinstance(rows, list) or not rows:
            raise ValueError('trigger report requires results')
        cards = []
        for row in rows:
            if row.get('status') not in ('complete', 'incomplete') or (row['status'] == 'incomplete' and row.get('pass') is not None) or (row['status'] == 'complete' and type(row.get('pass')) is not bool):
                raise ValueError('incomplete probes cannot pass or fail')
            cards.append((row['query'], row['status'], row['query'],
                          json.dumps(row.get('attempts', []), ensure_ascii=False, indent=2),
                          '判断：' + ('执行不完整' if row.get('pass') is None else '通过' if row['pass'] else '未通过')))
        summary = {'completed': sum(r['status'] == 'complete' for r in rows),
                   'incomplete': sum(r['status'] == 'incomplete' for r in rows),
                   'passed': sum(r.get('pass') is True for r in rows),
                   'failed': sum(r.get('pass') is False for r in rows)}
    else:
        raise ValueError('unknown result kind')
    sections = []
    for index, (label, status, prompt, output, evidence) in enumerate(cards):
        identity = hashlib.sha256((str(index) + label).encode()).hexdigest()[:16]
        status = {'ok': '完成', 'error': '执行失败', 'timeout': '超时', 'complete': '完成', 'incomplete': '执行不完整'}.get(status, status)
        sections.append(f'''<article><h2>{escape(label)}</h2><p class="status">执行状态：{escape(status)}</p>
<details><summary>任务输入</summary><pre>{escape(prompt)}</pre></details>
<details open><summary>实际输出</summary><pre>{escape(output)}</pre></details>
<details open><summary>判断依据</summary><pre>{escape(evidence)}</pre></details>
<label>你的判断 <select data-choice="{identity}"><option value="unreviewed">待评</option><option value="accept">通过</option><option value="revise">需修改</option></select></label>
<label>反馈 <textarea data-feedback="{identity}" rows="3"></textarea></label></article>''')
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>技能评测结果</title><style>
body{font-family:system-ui,sans-serif;color:#18212b;background:#f5f6f8;margin:0;line-height:1.6}main{max-width:960px;margin:auto;padding:24px}h1{font-size:25px;margin:0}h2{font-size:18px;margin:0;overflow-wrap:anywhere}article{background:white;border:1px solid #d8dee7;border-radius:8px;padding:20px;margin:16px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f8fa;padding:12px;font-size:13px}label{display:block;margin-top:12px}textarea{box-sizing:border-box;width:100%;font:inherit;padding:8px;border:1px solid #aab4c2;border-radius:4px}select,button{font:inherit;padding:7px 12px}button{color:white;background:#235ba8;border:0;border-radius:4px;cursor:pointer}summary{cursor:pointer}button:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid #508de0;outline-offset:2px}.status{color:#536174;margin:4px 0 12px}@media(max-width:600px){main{padding:14px}article{padding:14px}}
</style><main><h1>技能评测结果</h1><p>对照实际输出与判断依据。执行不完整的记录不计为通过。</p>
<details><summary>统计与覆盖范围</summary><pre>''' + escape(json.dumps(summary, ensure_ascii=False, indent=2)) + '</pre></details>' + ''.join(sections) + '''
<button id="generate-feedback">生成反馈</button><p>反馈只保留在本页。生成后可复制并保存，页面不会发送数据或修改原文件。</p>
<label for="feedback-preview">反馈内容</label><textarea id="feedback-preview" rows="8" readonly hidden></textarea></main>
<script>
document.getElementById('generate-feedback').addEventListener('click',()=>{
const feedback=Array.from(document.querySelectorAll('[data-feedback]')).map(node=>({id:node.dataset.feedback,judgment:document.querySelector('[data-choice="'+node.dataset.feedback+'"]').value,note:node.value}));
const preview=document.getElementById('feedback-preview');preview.value=JSON.stringify({feedback},null,2);preview.hidden=false;
});
</script></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--candidate', default='candidate')
    parser.add_argument('--baseline', default='baseline')
    args = parser.parse_args()
    try:
        if args.output.exists() or args.output.is_symlink():
            raise ValueError('output already exists; choose a new review file')
        document = render(json.loads(args.results.read_text(encoding='utf-8')), args.candidate, args.baseline)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as stream:
            stream.write(document)
        print(args.output)
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
