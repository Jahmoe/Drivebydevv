/* -------------------------------------------------------------
   Vehicle make & model prediction with TensorFlow.js
-------------------------------------------------------------- */

// 1) constants
const MODEL_PATH  = 'web_model/model.json';   // keep path exactly like this
const IMAGE_SIZE  = 224;                      // size used in training
const CLASS_NAMES = [
    'Acura MDX', 'Acura RDX', 'Audi A3', /* …all 196 labels in order… */
  ];
  

// cached model
let modelPromise;

// helper: lazy‑load model
function loadModel() {
  if (!modelPromise) {
    document.getElementById('loading').style.display = 'block';
    modelPromise = tf.loadLayersModel(MODEL_PATH).finally(
      () => (document.getElementById('loading').style.display = 'none')
    );
  }
  return modelPromise;
}

// image picker → preview
document.getElementById('imageUpload').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = ev => {
    const img = document.getElementById('preview');
    img.src = ev.target.result;
    img.classList.remove('hidden');
    document.getElementById('result').textContent = 'Ready to predict…';
  };
  reader.readAsDataURL(file);
});

// predict on click
async function predictVehicle() {
  const preview = document.getElementById('preview');
  if (preview.classList.contains('hidden')) {
    alert('Please choose an image first.'); return;
  }

  const resultBox = document.getElementById('result');
  resultBox.textContent = 'Predicting…';
  document.getElementById('loading').style.display = 'block';
  await tf.nextFrame();                      // let spinner display

  const model = await loadModel();

  // preprocess: jpeg → tensor → [1,224,224,3] float 0‑1
  const logits = tf.tidy(() => {
    const t = tf.browser.fromPixels(preview)
      .resizeBilinear([IMAGE_SIZE, IMAGE_SIZE])
      .toFloat()
      .div(255)
      .expandDims();
    return model.predict(t);
  });

  const probs = await logits.data();
  logits.dispose();

  const bestIdx = probs.indexOf(Math.max(...probs));
  const label   = CLASS_NAMES[bestIdx] ?? `Class #${bestIdx}`;
  const conf    = (probs[bestIdx] * 100).toFixed(2);

  document.getElementById('loading').style.display = 'none';
  resultBox.textContent = `${label} — ${conf}%`;
}

// make global for inline HTML onclick
window.predictVehicle = predictVehicle;
