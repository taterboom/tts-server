generate

```
JSON.stringify(`zh-TW-HsiaoChenNeural (Female)
zh-TW-HsiaoYuNeural (Female)
zh-TW-YunJheNeural (Male)`.split('\n').map(item => {
    const result = item.match(/([a-zA-Z\-]+)\s\(([a-zA-Z,\s]+)\)/)
    if (!result) return null
    return [result[1], result[2]]
}).map(([id, t]) => ({id, t, r: 'zh-CN', n: ""})))
```

decode in client

```
fetch('/tts-enc', {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({text: "hello S3", speaker: "en-US-JessaNeural"})
}).then(res => res.text()).then((b) =>
    actx.decodeAudioData(new Uint8Array(b.split('').reduce((a, b) => {
        if (a[a.length - 1]?.length === 1) {
            a[a.length - 1] += b
        } else {
            a[a.length] = b
        }
        return a
    }, []).map(item => parseInt(item, 16))).buffer)
).then(buf => {
    const source = actx.createBufferSource();
    source.buffer = buf;
    source.connect(actx.destination);
    source.start();
})
```
