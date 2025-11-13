
import React, { useState } from 'react';

export default function UploadForm() {
  const [mix, setMix] = useState(null);
  const [target, setTarget] = useState(null);
  const [result, setResult] = useState(null);

  const submit = async () => {
    const form = new FormData();
    form.append("mixture", mix);
    form.append("target", target);
    const res = await fetch("/process", {
      method: "POST",
      body: form
    });
    const json = await res.json();
    setResult(json);
  };

  return (
    <div>
      <input type="file" accept="audio/*" onChange={e => setMix(e.target.files[0])} />
      <br/>
      <input type="file" accept="audio/*" onChange={e => setTarget(e.target.files[0])} />
      <br/>
      <button onClick={submit}>Process</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
