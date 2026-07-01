const WS_URL = "ws://localhost:8765";
const MIC_MAX_RMS = 0.05;
const CAM_HEADER = new Uint8Array([0x43, 0x41, 0x4d, 0x00]); // "CAM\0"
const CAM_FPS = 5;

let ws, micCtx, playCtx, processor, playCursor = 0;
let scheduledSources = [];

document.getElementById("startBtn").onclick = start;
document.getElementById("photoBtn").onclick = () => {
  if (ws && ws.readyState === WebSocket.OPEN) ws.send("PHOTO");
};
document.getElementById("taskAddBtn").onclick = () => {
  const input = document.getElementById("taskInput");
  if (input.value.trim()) {
    sendTaskCmd({ action: "add", text: input.value.trim() });
    input.value = "";
  }
};

async function start() {
  document.getElementById("startBtn").style.display = "none";
  document.getElementById("statusRow1").style.display = "flex";
  document.getElementById("statusRow2").style.display = "flex";
  document.getElementById("taskPanel").style.display = "block";

  ws = new WebSocket(WS_URL);
  ws.binaryType = "arraybuffer";
  ws.onmessage = onMessage;
  ws.onopen = () => console.log("[WS] połączono");
  ws.onclose = () => console.log("[WS] rozłączono");

  playCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
  playCursor = playCtx.currentTime;

  micCtx = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
  const micStream = await navigator.mediaDevices.getUserMedia({
    audio: { channelCount: 1, sampleRate: 16000 },
  });
  const source = micCtx.createMediaStreamSource(micStream);
  processor = micCtx.createScriptProcessor(1024, 1, 1);
  processor.onaudioprocess = onAudioProcess;

  // ScriptProcessorNode musi być podłączony do destination żeby odpalać callback,
  // ale gain=0 żeby nie było echo mikrofonu w głośnikach.
  const silentGain = micCtx.createGain();
  silentGain.gain.value = 0;
  source.connect(processor);
  processor.connect(silentGain);
  silentGain.connect(micCtx.destination);

  await startCamera();
}

async function startCamera() {
  const video = document.getElementById("camPreview");
  const canvas = document.getElementById("camCanvas");
  const ctx = canvas.getContext("2d");

  const camStream = await navigator.mediaDevices.getUserMedia({
    video: { width: 320, height: 240 },
  });
  video.srcObject = camStream;
  document.getElementById("camWrap").style.display = "block";
  document.getElementById("photoBtn").style.display = "block";

  setInterval(() => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(async (blob) => {
      if (!blob) return;
      const jpegBytes = new Uint8Array(await blob.arrayBuffer());
      const frame = new Uint8Array(CAM_HEADER.length + jpegBytes.length);
      frame.set(CAM_HEADER, 0);
      frame.set(jpegBytes, CAM_HEADER.length);
      ws.send(frame.buffer);
    }, "image/jpeg", 0.7);
  }, 1000 / CAM_FPS);
}

function onAudioProcess(e) {
  const input = e.inputBuffer.getChannelData(0);
  let sumSquares = 0;
  const pcm16 = new Int16Array(input.length);
  for (let i = 0; i < input.length; i++) {
    const s = Math.max(-1, Math.min(1, input[i]));
    pcm16[i] = s * 32767;
    sumSquares += s * s;
  }
  const rms = Math.sqrt(sumSquares / input.length);
  document.getElementById("micBar").style.width = Math.min(100, (rms / MIC_MAX_RMS) * 100) + "%";
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(pcm16.buffer);
  }
}

function onMessage(e) {
  if (typeof e.data === "string") {
    if (e.data === "STOP") {
      for (const src of scheduledSources) {
        try { src.stop(0); } catch (_) {}
      }
      scheduledSources = [];
      playCursor = playCtx.currentTime;
    } else if (e.data.startsWith("STATE:")) {
      const state = e.data.split(":")[1];
      document.getElementById("spkDot").style.background = state === "speak" ? "#0c4" : "#444";
    } else if (e.data.startsWith("FACE:")) {
      drawFaceBox(e.data.slice(5));
    } else if (e.data.startsWith("TASKS:")) {
      renderTasks(JSON.parse(e.data.slice(6)));
    }
    return;
  }
  playChunk(e.data);
}

function sendTaskCmd(cmd) {
  if (ws && ws.readyState === WebSocket.OPEN) ws.send("TASK:" + JSON.stringify(cmd));
}

function renderTasks(tasks) {
  const list = document.getElementById("taskList");
  list.innerHTML = "";
  for (const t of tasks) {
    const row = document.createElement("div");
    row.className = "task-row";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = t.status === "done";
    cb.onchange = () => sendTaskCmd({ action: "toggle", id: t.id });

    const label = document.createElement("span");
    label.textContent = t.text;
    label.style.textDecoration = t.status === "done" ? "line-through" : "none";
    label.onclick = () => {
      const nt = prompt("Edytuj zadanie:", t.text);
      if (nt && nt.trim()) sendTaskCmd({ action: "edit", id: t.id, text: nt.trim() });
    };

    const del = document.createElement("button");
    del.textContent = "×";
    del.onclick = () => sendTaskCmd({ action: "delete", id: t.id });

    row.append(cb, label, del);
    list.appendChild(row);
  }
}

function drawFaceBox(payload) {
  const canvas = document.getElementById("faceOverlay");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  if (payload === "none") return;

  const [nx1, ny1, nx2, ny2, label] = payload.split(",");
  const x1 = parseFloat(nx1) * canvas.width;
  const y1 = parseFloat(ny1) * canvas.height;
  const x2 = parseFloat(nx2) * canvas.width;
  const y2 = parseFloat(ny2) * canvas.height;
  const igor = label === "Igor";

  ctx.strokeStyle = igor ? "#0c4" : "#c00";
  ctx.lineWidth = 2;
  ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
  ctx.fillStyle = igor ? "#0c4" : "#c00";
  ctx.font = "14px sans-serif";
  ctx.fillText(label, x1, y1 - 4);
}

function playChunk(arrayBuffer) {
  const pcm16 = new Int16Array(arrayBuffer);
  const float32 = new Float32Array(pcm16.length);
  for (let i = 0; i < pcm16.length; i++) float32[i] = pcm16[i] / 32768;

  const buffer = playCtx.createBuffer(1, float32.length, 24000);
  buffer.copyToChannel(float32, 0);

  const src = playCtx.createBufferSource();
  src.buffer = buffer;
  src.connect(playCtx.destination);

  const startAt = Math.max(playCursor, playCtx.currentTime);
  src.start(startAt);
  playCursor = startAt + buffer.duration;
  scheduledSources.push(src);
  src.onended = () => {
    scheduledSources = scheduledSources.filter((s) => s !== src);
  };
}
