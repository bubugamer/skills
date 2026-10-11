---
name: wait-what
description: Re-explain the previous answer when the user says they did not understand, asks to re-pitch, or invokes wait-what. Use plain language and the language of the current conversation.
---

补足上下文后，重新解释上一段回答。默认跟随当前对话语言；中文对话用自然中文。
先说目前结论，再解释它与用户目标的关系，用一个具体例子说明。
已有 GLOSSARY.md 时使用其中的术语；多个词汇表按 GLOSSARY-MAP.md 选择。
只回应本次理解困难，不把重讲扩展为新的执行任务。
完成条件：读者能知道我们正在解决什么、已经得到什么结论、下一步为什么必要。
