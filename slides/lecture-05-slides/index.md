<section class="title">
  <div class="title-main">Lecture 05 - Attention and Transformers</div>
  <div class="title-sub">DATA130030.01 (自然语言处理)</div>
  <div class="title-meta">
    <div>Baojian Zhou</div>
    <div>School of Data Science</div>
    <div>Fudan University</div>
    <div>04/02/2026</div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Outline</div>
  <div class="ppt-line"></div>
  <ul class="outline-bullets big">
    <li class="active">Encoder-decoder model</li>
    <li class="muted">Attention mechanism</li>
    <li class="muted">Self-attention</li>
    <li class="muted">Transformer</li>
  </ul>
</section>

---

<section class="ppt">
  <div class="ppt-title">Encoder-Decoder Model</div>
  <div class="ppt-line"></div>
  <div style="margin-bottom: 18px; font-size: 32px; line-height: 1.5;">
    <ul style="margin: 0; padding-left: 1.1em;">
      <li>Key idea: Use an <b>encoder</b> network that takes \(\boldsymbol{x}_{1:n}\) and creates a contextualized representation. This context is passed to a <b>decoder</b> which generates a task-specific \(\boldsymbol{z}_{1:m}\)</li>
    </ul>
  </div>
  <div style="display:flex; gap:3rem; align-items:flex-start;">
    <!-- Left: Architecture Diagram -->
    <div style="flex:1; display:flex; flex-direction:column; align-items:center; font-size:26px;">
      <!-- Output labels -->
      <div style="display:flex; justify-content:space-around; width:100%; margin-bottom:4px;">
        <span>\(\boldsymbol{z}_1\)</span>
        <span>\(\boldsymbol{z}_2\)</span>
        <span>\(\cdots\)</span>
        <span>\(\boldsymbol{z}_m\)</span>
      </div>
      <!-- Upward arrows from decoder -->
      <div style="display:flex; justify-content:space-around; width:100%; line-height:1;">
        <span>↑</span><span>↑</span><span></span><span>↑</span>
      </div>
      <!-- Decoder box -->
      <div style="background:#c8e6c9; border:2px solid #888; border-radius:6px; width:100%; text-align:center; padding:14px 0; font-size:28px; margin-bottom:0;">
        Decoder
      </div>
      <!-- Arrow up to decoder -->
      <div style="font-size:22px; line-height:1.6;">↑</div>
      <!-- Context box -->
      <div style="background:#ffcc99; border:2px solid #888; border-radius:6px; width:75%; text-align:center; padding:12px 0; font-size:28px; margin-bottom:0;">
        Context
      </div>
      <!-- Arrow up to context -->
      <div style="font-size:22px; line-height:1.6;">↑</div>
      <!-- Encoder box -->
      <div style="background:#aec6e8; border:2px solid #888; border-radius:6px; width:100%; text-align:center; padding:14px 0; font-size:28px; margin-bottom:0;">
        Encoder
      </div>
      <!-- Upward arrows from inputs -->
      <div style="display:flex; justify-content:space-around; width:100%; line-height:1.6;">
        <span>↑</span><span>↑</span><span></span><span>↑</span>
      </div>
      <!-- Input labels -->
      <div style="display:flex; justify-content:space-around; width:100%; margin-top:2px;">
        <span>\(\boldsymbol{x}_1\)</span>
        <span>\(\boldsymbol{x}_2\)</span>
        <span>\(\cdots\)</span>
        <span>\(\boldsymbol{x}_n\)</span>
      </div>
    </div>
    <!-- Right: Bullet points -->
    <div style="flex:1.2; font-size:28px; line-height:1.45;">
      <ul style="margin: 0; padding-left: 1.1em;">
        <li style="margin-bottom:12px;"><b>Encoder</b> (LSTMs, CNNs, and Transformers)
          <ul style="font-size:0.9em; margin-top:6px; line-height:1.35;">
            <li>Accepts an input sequence, \(\boldsymbol{x}_{1:n}\)</li>
            <li>Generates a sequence of contextualized representations, \(\boldsymbol{h}_{1:n}\)</li>
          </ul>
        </li>
        <li style="margin-bottom:12px;"><b>Context</b>
          <ul style="font-size:0.9em; margin-top:6px; line-height:1.35;">
            <li>A function of \(\boldsymbol{h}_{1:n}\), and conveys the essence of \(\boldsymbol{x}_{1:n}\)</li>
            <li>Generates a context vector \(\boldsymbol{c}\)</li>
          </ul>
        </li>
        <li style="margin-bottom:12px;"><b>Decoder</b> (LSTMs, CNNs, and Transformers)
          <ul style="font-size:0.9em; margin-top:6px; line-height:1.35;">
            <li>Accepts \(\boldsymbol{c}\) as input and generates a sequence of hidden states \(\boldsymbol{h}_{1:m}\) from which a corresponding sequence of output \(\boldsymbol{z}_{1:m}\)</li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Encoder-Decoder Model (MT)</div>
  <div class="ppt-line"></div>
  <div style="font-size:32px; line-height:1.5;">
    <ul style="margin: 0 0 10px 0; padding-left: 1.1em;">
      <li>Machine translation (MT) task:</li>
    </ul>
    <div style="text-align:center; font-size:32px; margin: 10px 0 18px 0;">
      <span style="color:#4caf50;">je suis étudiant</span>
      <span style="color:#333;"> -> </span>
      <span style="color:#7b3fa0;"><u>i</u> am a student</span>
    </div>
    <div style="font-size:29px; line-height:1.55; margin-bottom:18px;">
      The encoder and decoder tend to both be recurrent neural networks (e.g., LSTM). <br>
      The context would be of a size like 256, 512, or 1024
    </div>
  </div>
  
  <!-- 视频演示 -->
  <div style="display:flex; flex-direction:column; align-items:center; margin-top:8px;">
<video 
  src="media/ppt/media/1.mp4"
  autoplay loop muted playsinline
  style="width:auto; max-width:100%; height:auto;"
></video>
    <div style="font-size:18px; margin-top:10px;">
      <a href="https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/" style="color:#1a73e8;">
        https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/
      </a>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">RNN-based encoder-decoder nets</div>
  <div class="ppt-line"></div>
  <div style="display:flex; gap:2rem; align-items:flex-start; margin-bottom:18px;">
    <!-- Left: bullet text -->
    <div style="flex:1.1; font-size:36px; line-height:1.5;">
      <ul style="margin:0; padding-left:1.1em;">
        <li>Sutskever et al. (2014) then showed how to use extended RNNs for both encoder and decoder</li>
      </ul>
    </div>
    <!-- Right: paper figure -->
    <div style="flex:1; font-size:16px; line-height:1.3; text-align:left;">
      <img
        src="media/ppt/media/图片1.png"
        alt="Sutskever et al. 2014 sequence to sequence figure"
        style="width:80%; border:none; box-shadow:none; background:none; margin-bottom:6px;"
      >
    </div>
  </div>
  <!-- 视频演示 -->
  <div style="display:flex; flex-direction:column; align-items:center; margin-top:3px;">
<video 
  src="media/ppt/media/2.mp4"
  autoplay loop muted playsinline
  style="width:auto; max-width:70%; height:auto;"
></video>
  </div>
  <!-- Bottom row -->
  <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-top:5px; font-size:20px;">
    <div style="display:flex; gap:5rem; padding-left:4rem;">
    </div>
    <div style="font-size:15px; text-align:right; color:#333;">
      Sequence to Sequence Learning with<br>
      Neural Networks (<a href="https://arxiv.org/abs/1409.3215" style="color:#1a73e8;">Sutskever et al., 2014</a>)
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Translating a single sentence</div>
  <div class="ppt-line"></div>
  <div style="font-size:30px; line-height:1.5;">
    <div style="font-size:30px; line-height:1.55; margin-bottom:0px;">
Use the superscripts 𝑒 and 𝑑 where needed to distinguish the hidden states of the encoder and the decoder
  </div>
  
<!-- 视频演示改为图片演示 -->
<div style="display:flex; flex-direction:column; align-items:center; margin-top:0px;">
  <img 
    src="media/ppt/media/图片2.png"
    alt="Neural Machine Translation Sequence to Sequence Model"
    style="width:auto; max-width:90%; height:auto; border-radius:12px;"
  >
</div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Bottleneck of RNN-based Encoder-Decoder</div>
  <div class="ppt-line"></div>
  <div style="font-size:30px; line-height:1.5;">
    <div style="font-size:36px; line-height:1.55; margin-bottom:0px;">
Context is $c = h_n^e$, the hidden state of the last (𝑛-th) time step of the source text. This final hidden state is thus acting as a bottleneck
  </div>
  
<!-- 视频演示改为图片演示 -->
<div style="display:flex; flex-direction:column; align-items:center; margin-top:10px;">
  <img 
    src="media/ppt/media/图片3.png"
    alt="Neural Machine Translation Sequence to Sequence Model"
    style="width:auto; max-width:100%; height:auto; border-radius:12px;"
  >
</div>

<div style="font-size:30px; line-height:1.5;">
    <div style="font-size:36px; line-height:1.55; margin-bottom:10px;">
The <b>attention mechanism</b>, as in the vanilla encoder-decoder model, the context $c$ is a function of hidden states  

$$ c = f(h_1^e, h_2^e, \dots, h_n^e) $$
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Context vector \(c_i\)</div>
  <div class="ppt-line"></div>
  <div style="display:flex; gap:2rem; align-items:flex-start;">
    <div style="flex:1.1; font-size:30px; line-height:1.5;">
      <ul style="margin:0 0 10px 0; padding-left:1.1em;">
        <li style="margin-bottom:10px;">
          \(\alpha_{ij}\): the proportional relevance of each encoder hidden state \(\boldsymbol{h}_j^e\) to the prior hidden decoder state \(\boldsymbol{h}_{i-1}^d\)
        </li>
      </ul>
      <div style="text-align:center; font-size:28px; margin: 10px 0 18px 2rem;">
        \(\alpha_{ij} = \text{softmax}\!\left(\text{score}(\boldsymbol{h}_{i-1}^d, \boldsymbol{h}_j^e)\right) \; \forall j \in e\)
      </div>
      <div style="text-align:center; font-size:28px; margin: 0 0 22px 2rem;">
        $$\alpha_{ij} = \frac{\exp\!\left(score\!\left(\boldsymbol{h}_{i-1}^d,\, \boldsymbol{h}_j^e\right)\right)}{\sum_k \exp\!\left(score\!\left(\boldsymbol{h}_{i-1}^d,\, \boldsymbol{h}_k^e\right)\right)}$$
      </div>
      <ul style="margin:0 0 10px 0; padding-left:1.1em;">
        <li style="margin-bottom:10px;">
          Fixed-length context vector for the current decoder state by taking a weighted average over all the encoder hidden states
        </li>
      </ul>
      <div style="text-align:center; font-size:28px; margin: 10px 0 0 2rem;">
        $$\boldsymbol{c}_i = \sum_j \alpha_{ij}\, \boldsymbol{h}_j^e$$
      </div>
    </div>
    <div style="flex:1; display:flex; align-items:center; justify-content:center;">
      <img
        src="media/ppt/media/图片4.png"
        alt="Attention mechanism diagram"
        style="width:120%; max-width:690px; border:none; box-shadow:none; background:none;"
      >
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Outline</div>
  <div class="ppt-line"></div>
  <ul class="outline-bullets big">
    <li class="muted">Encoder-decoder model</li>
    <li class="active">Attention mechanism</li>
    <li class="muted">Self-attention</li>
    <li class="muted">Transformer</li>
  </ul>
</section>

---

<section class="ppt">
  <div class="ppt-title">
  Attention mechanism 
  <span style="font-size: 0.7em; color:#4caf50;">Intuition</span>
</div>
  <div class="ppt-line"></div>
  <div style="font-size:32px; line-height:1.5;">
    <div style="font-size:29px; line-height:1.55; margin-bottom:0px;">
<b>Time series prediction</b>
  </div>

<div style="font-size:36px; line-height:1.55; margin-bottom:0px;">
<li>Suppose we have a time series of data points (noisy)
  </div>
  
<!-- 视频演示改为图片演示 -->
<div style="display:flex; flex-direction:column; align-items:center; margin-top:10px;">
  <img 
    src="media/ppt/media/图片5.png"
    alt="Neural Machine Translation Sequence to Sequence Model"
    style="width:auto; max-width:60%; height:auto; border-radius:12px;"
  >
</div>

<div style="font-size:32px; line-height:1.5;">
    <div style="font-size:36px; line-height:1.55; margin-bottom:10px;">
<li>Can we design a method so that we can reduce the noise in 𝒙_𝑖 so that output timeseries data look smooth?
  </div>

<div style="position: absolute; top: 10px; right: 20px; font-size: 18px;">
  <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">
    Rasa Algorithm Whiteboard
  </a>
</div>
</section>

---


<section class="ppt">
  <div class="ppt-title">Attention mechanism <span style="color:#4caf50;">Intuition</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; gap:2rem; align-items:flex-start;">
    <div style="flex:1.1; font-size:32px; line-height:1.5;">
      <div style="font-size:29px; margin-bottom:12px;"><b>Time series prediction</b></div>
      <img
        src="media/ppt/media/图片6.png"
        alt="Time series prediction chart"
        style="width:100%; border:none; box-shadow:none; background:none;"
      >
    </div>
    <div style="flex:1; font-size:32px; line-height:1.55; margin-top: 32px;">
      <ul style="margin:0 0 6px 0; padding-left:1.1em;">
        <li style="margin-bottom:4px;">Time series data</li>
      </ul>
      <div style="text-align:center; margin:6px 0 4px 0; color:#1a73e8; font-size:32px;">
        $$\boldsymbol{x} = [x_0, x_1, x_2, \dots, x_i, \dots, x_n]$$
      </div>
      <ul style="margin:0 0 14px 0; padding-left:2.2em;">
        <li style="margin-bottom:4px;">These data points are noisy</li>
      </ul>
      <ul style="margin:0 0 14px 0; padding-left:1.1em;">
        <li style="margin-bottom:4px;"><b>Task</b>: Reduce noise so that points have <span style="color:red;">more context and more robust signal</span></li>
      </ul>
      <ul style="margin:0 0 6px 0; padding-left:1.1em;">
        <li style="margin-bottom:4px;"><b>Goal</b>: get fitting values</li>
      </ul>
      <div style="text-align:center; margin:6px 0 0 0; color:#e59400; font-size:32px;">
        $$Z = [z_0, z_1, z_2, \dots, z_i, \dots, z_n]$$
      </div>
    </div>
  </div>

<div style="position: absolute; top: 10px; right: 20px; font-size: 18px;">
  <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">
    Rasa Algorithm Whiteboard
  </a>
</div>

</section>


---

<section class="ppt">
  <div class="ppt-title">Attention mechanism <span style="color:#4caf50;">Intuition</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start; margin-bottom:18px;">
      <div style="flex:1.1; font-size:32px; line-height:1.5;">
        <div style="font-size:29px; margin-bottom:12px;"><b>Time series prediction</b></div>
        <img src="media/ppt/media/图片7.png" alt="Time series prediction chart" style="width:100%; border:none; box-shadow:none; background:none;">
      </div>
      <div style="flex:1; font-size:32px; line-height:1.55;margin-top: 30px;">
        <ul style="margin:0 0 8px 0; padding-left:1.1em;">
          <li style="margin-bottom:4px;">Time series noisy data:</li>
        </ul>
        <div style="text-align:center; margin:4px 0 18px 0; color:#1a73e8; font-size:32px;">
          $$\boldsymbol{x} = [x_0, x_1, x_2, \dots, x_i, \dots, x_n]$$
        </div>
        <ul style="margin:0 0 8px 0; padding-left:1.1em;">
          <li style="margin-bottom:4px;">Time series true data:</li>
        </ul>
        <div style="text-align:center; margin:4px 0 0 0; color:#1a73e8; font-size:32px;">
          $$\boldsymbol{z} = [z_0, z_1, z_2, \dots, z_i, \dots, z_n]$$
        </div>
      </div>
    </div>
    <div style="font-size:36px; line-height:1.55;">
      <ul style="margin:0; padding-left:1.1em;">
        <li style="margin-bottom:10px;">Key observation: the true value \(y_i\) of each noisy point \(i\) depends on noisy data \(x_i\) itself and other data points</li>
        <li>Many methods we can choose, but try <span style="color:red; font-weight:bold;">re-weighing</span></li>
      </ul>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---



<section class="ppt">
  <div class="ppt-title">Attention mechanism <span style="color:#4caf50;">Intuition</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start;">
      <div style="flex:1.1; font-size:30px; line-height:1.5;">
        <div style="font-size:32px; margin-bottom:12px;"><b>Time series prediction</b></div>
        <img src="media/ppt/media/图片8.png" alt="Time series prediction chart" style="width:100%; border:none; box-shadow:none; background:none;">
      </div>
      <div style="flex:1; font-size:36px; line-height:1.55;margin-top: 30px;">
        <ul style="margin:0 0 18px 0; padding-left:1.1em;">
          <li>Time series data \(\boldsymbol{x} = [x_{0:n}]\)</li>
        </ul>
        <ul style="margin:0 0 6px 0; padding-left:1.1em;">
          <li><b>Re-weighing vector</b> for \(x_i\)</li>
        </ul>
        <div style="text-align:center; margin:2px 0 18px 0; color:#4caf50; font-size:27px;">
          $$\boldsymbol{w}_i = [w_{0:n,i}]$$
        </div>
        <ul style="margin:0 0 14px 0; padding-left:1.1em;">
          <li>Re-weighing vector \(\boldsymbol{w}_i\) has higher magnitudes near \(x_i\)</li>
        </ul>
        <ul style="margin:0; padding-left:1.1em;">
          <li>So, re-weighing vector is a kind of "<span style="color:red; font-weight:bold;">Attention</span>" of \(x_i\)</li>
        </ul>
      </div>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>


---


<section class="ppt">
  <div class="ppt-title">Attention mechanism <span style="color:#4caf50;">Intuition</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start;">
      <div style="flex:1.1; font-size:32px; line-height:1.5;">
        <div style="font-size:36px; margin-bottom:12px;"><b>Time series prediction</b></div>
        <img src="media/ppt/media/图片9.png" alt="Time series prediction chart" style="width:100%; border:none; box-shadow:none; background:none;">
      </div>
      <div style="flex:1; font-size:32px; line-height:1.8; margin-top:36px;">
        <ul style="margin:0 0 20px 0; padding-left:1.1em;">
          <li style="color:red; font-weight:bold; font-size:40px; list-style-type:disc;">Idea of re-weighing</li>
        </ul>
        <ul style="margin:0 0 10px 0; padding-left:1.1em; font-size:36px;">
          <li>Time series data: \(\boldsymbol{x} = \) <span style="color:#1a73e8;">\([x_{0:n}]\)</span></li>
          <li>Re-weighing: \(\boldsymbol{w}_i = \) <span style="color:#4caf50;">\([w_{0:n,i}]\)</span></li>
          <li>Each \(w_{ji}\): weight of point \(x_j\)</li>
        </ul>
  <div style="text-align:center; margin:24px 0 0 0; font-size:36px; font-weight:bold;">
    $$\color{#e59400}{z_i} = \color{#4caf50}{\boldsymbol{w}_i} \cdot \color{#1a73e8}{\boldsymbol{x}}$$
  </div>
      </div>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>


---

<section class="ppt">
  <div class="ppt-title">Attention mechanism <span style="color:#4caf50;">Intuition</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start;">
      <div style="flex:1.1; font-size:30px; line-height:1.5;">
        <div style="font-size:36px; margin-bottom:12px;"><b>Time series prediction</b></div>
        <img src="media/ppt/media/图片10.png" alt="Time series prediction chart" style="width:90%; border:none; box-shadow:none; background:none;">
      </div>
      <div style="flex:1; font-size:36px; line-height:1.8; margin-top:10px;">
        <ul style="margin:0 0 24px 0; padding-left:1.1em;">
        <li style="color:red; font-weight:bold; font-size:40px;">Idea of re-weighing</li>
        </ul>
        <div>
        <ul style="margin:0 0 0 0; padding-left:2em; font-size:28px; line-height:1.7;">
          <li style="margin-bottom:10px;">Time series data:</li>
        </ul>
        <div style="color:#1a73e8; font-size:26px; margin:2px 0 12px 2.5em;">
          $$\boldsymbol{x} = [x_0, x_1, x_2, \dots, x_i, \dots, x_n]$$
        </div>
        <ul style="margin:0 0 0 0; padding-left:2em; font-size:28px; line-height:1.7;">
          <li style="margin-bottom:2px;">Re-weighing vector</li>
        </ul>
        <div style="color:#4caf50; font-size:26px; margin:2px 0 12px 2.5em;">
          $$\boldsymbol{w}_i = [w_{0i}, w_{1i}, w_{2i}, \dots, w_{ii}, \dots, w_{ni}]$$
        </div>
        <ul style="margin:0 0 0 0; padding-left:2em; font-size:28px; line-height:1.7;">
          <li style="margin-bottom:2px;">Each \(w_{ji}\): the weight of point \(x_j\)</li>
          <li style="margin-bottom:2px;">Fitting value</li>
        </ul>
        <div style="font-size:28px; margin:4px 0 0 2.5em;">
          $$\color{#e59400}{z_i} = \color{#4caf50}{\boldsymbol{w}_i} \cdot \color{#1a73e8}{\boldsymbol{x}},\; \color{#e59400}{\boldsymbol{i}} \ \color{black}{from} \ \color{#e59400}{0\;1\;2} \ \color{black}{to} \ \color{#e59400}{n}$$
        </div>
      </div>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Attention mechanism <span style="color:#4caf50;">Intuition</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start;">
      <div style="flex:1.1; font-size:30px; line-height:1.5;">
        <div style="font-size:36px; margin-bottom:12px;"><b>Time series prediction</b></div>
        <img src="media/ppt/media/图片10.png" alt="Time series prediction chart" style="width:90%; border:none; box-shadow:none; background:none;">
      </div>
      <div style="flex:1; font-size:28px; line-height:1.8; margin-top:10px;">
        <!-- 将所有列表项放在同一个 <ul> 内，便于统一控制间距 -->
        <ul style="margin:0; padding-left:1.1em; list-style-type:disc;">
          <li style="color:red; font-weight:bold; font-size:40px; margin-bottom:30px;">Idea of re-weighing</li>
          <li style="margin-bottom:20px;">\(\boldsymbol{W}\) filters datapoints which are far away from \(x_i\) but amplifies datapoints that are close to \(x_i\).</li>
          <li style="margin-bottom:20px;">Re-weighing is to find such reasonable “context” matrix \(\boldsymbol{W}\) so that we can get better signals by using contexts of data points.</li>
          <li><b>How can we apply this re-weighing to text data ?</b></li>
        </ul>
      </div>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Outline</div>
  <div class="ppt-line"></div>
  <ul class="outline-bullets big">
    <li class="muted">Encoder-decoder model</li>
    <li class="muted">Attention mechanism</li>
    <li class="activate">Self-attention</li>
    <li class="muted">Transformer</li>
  </ul>
</section>

---

<section class="ppt">
  <div class="ppt-title">Get more context for text</div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="font-size:36px; line-height:1.6;">
      <ul style="margin:0 0 6px 0; padding-left:1.1em;">
        <li style="margin-bottom:6px;">Get a more context for: <span style="color:#1a73e8; font-style:italic;">Noa can be <u>annoying</u> but she is a great cat</span></li>
        <li>Given the above, how can we get more and better context for these words, say <span style="color:#e59400;">annoying</span>?</li>
      </ul>
    </div>
    <div style="font-size:30px; margin:6px 0 10px 2em; color:#555;">
      Words closer to <span style="color:#1a73e8;">annoying</span> have more effects on the word <span style="color:#1a73e8;">annoying</span>
    </div>
    <div style="display:flex; justify-content:center; margin:0 0 10px 0;">
      <svg viewBox="0 0 900 200" xmlns="http://www.w3.org/2000/svg" style="width:95%; max-width:860px;">
        <style>
          .word { font-size: 28px; font-family: sans-serif; fill: #e59400; text-anchor: middle; }
          .word-focus { font-size: 28px; font-family: sans-serif; fill: #e59400; text-anchor: middle; font-weight: bold; }
        </style>
        <text x="60"  y="40" class="word">Noa</text>
        <text x="160" y="40" class="word">can</text>
        <text x="240" y="40" class="word">be</text>
        <text x="370" y="40" class="word-focus">annoying</text>
        <line x1="330" y1="46" x2="420" y2="46" stroke="#222" stroke-width="2.5"/>
        <text x="500" y="40" class="word">but</text>
        <text x="600" y="40" class="word">she</text>
        <text x="670" y="40" class="word">is</text>
        <text x="720" y="40" class="word">a</text>
        <text x="790" y="40" class="word">great</text>
        <text x="865" y="40" class="word">cat</text>
        <!-- 所有路径起点改为中心，终点改为外围词 -->
        <path d="M 370,48 Q 305,105 240,48" stroke="#3a5fa0" stroke-width="2.5" fill="none" marker-end="url(#arrowBlue)"/>
        <path d="M 370,48 Q 265,130 160,48" stroke="#6a8fc0" stroke-width="2" fill="none" marker-end="url(#arrowBlue2)"/>
        <path d="M 370,48 Q 435,105 500,48" stroke="#6a8fc0" stroke-width="2" fill="none" marker-end="url(#arrowBlue2)"/>
        <path d="M 370,48 Q 485,140 600,48" stroke="#9ab0d0" stroke-width="1.8" fill="none" marker-end="url(#arrowBlue3)"/>
        <path d="M 370,48 Q 520,155 670,48" stroke="#b0c4de" stroke-width="1.5" fill="none" marker-end="url(#arrowBlue4)"/>
        <path d="M 370,48 Q 215,175 60,48" stroke="#e53935" stroke-width="2.5" fill="none" marker-end="url(#arrowRed)"/>
        <path d="M 370,48 Q 617,175 865,48" stroke="#e53935" stroke-width="2.5" fill="none" marker-end="url(#arrowRed)"/>
        <defs>
          <marker id="arrowBlue"  markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3a5fa0"/></marker>
          <marker id="arrowBlue2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#6a8fc0"/></marker>
          <marker id="arrowBlue3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#9ab0d0"/></marker>
          <marker id="arrowBlue4" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#b0c4de"/></marker>
          <marker id="arrowRed"   markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#e53935"/></marker>
        </defs>
      </svg>
    </div>
    <div style="font-size:36px; font-weight:bold; line-height:1.5; margin-top:6px;">
      But the intuition tells that proximity might not be the best thing in language. Relations between words have to do with linguistic meaning and structures.
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Get more context for text</div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="font-size:36px; line-height:1.9;">
      <ul style="margin:0 0 8px 0; padding-left:1.1em;">
        <li>Get a more context for: <span style="color:#1a73e8; font-style:italic;">Noa can be <u>annoying</u> but she is a great cat</span></li>
      </ul>
    </div>
    <div style="font-size:36px; margin:2px 0 6px 1.8em; text-decoration:line-through; color:#888; line-height:1.7;">
      Words closer to <span style="color:#1a73e8;">annoying</span> have more effects on the word <span style="color:#1a73e8;">annoying</span>
    </div>
    <div style="font-size:36px; margin:2px 0 16px 1.8em; line-height:1.7;">
      Words <span style="color:#4caf50;">Noa</span>, <span style="color:#4caf50;">is</span> and <span style="color:#4caf50;">cat</span> are "closer" to <span style="color:#4caf50;">she</span>. So, we cannot blindly use proximity.
    </div>
    <div style="display:flex; justify-content:center;">
      <svg viewBox="0 0 1100 240" xmlns="http://www.w3.org/2000/svg" style="width:98%; max-width:980px;">
        <defs>
          <marker id="arrowGreen" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4caf50"/></marker>
          <marker id="arrowBlue1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#3a5fa0"/></marker>
          <marker id="arrowBlue2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#6a8fc0"/></marker>
          <marker id="arrowBlue3" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#9ab0d0"/></marker>
          <marker id="arrowBlue4" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#b8cce4"/></marker>
        </defs>
        <text x="80"  y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle">Noa</text>
        <text x="190" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle">can</text>
        <text x="295" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle">be</text>
        <text x="445" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle" font-weight="bold">annoying</text>
        <line x1="400" y1="126" x2="495" y2="126" stroke="#222" stroke-width="2.5"/>
        <text x="580" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle">but</text>
        <text x="690" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle" font-weight="bold">she</text>
        <line x1="660" y1="126" x2="722" y2="126" stroke="#4caf50" stroke-width="2.5"/>
        <text x="780" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle">is</text>
        <text x="850" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle">a</text>
        <text x="940" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle">great</text>
        <text x="1040" y="120" font-size="30" font-family="sans-serif" fill="#e59400" text-anchor="middle" font-weight="bold">cat</text>
        <path d="M 680,105 Q 380,10 90,105" stroke="#4caf50" stroke-width="2.5" fill="none" marker-end="url(#arrowGreen)"/>
        <path d="M 700,105 Q 740,55 770,105" stroke="#4caf50" stroke-width="2.5" fill="none" marker-end="url(#arrowGreen)"/>
        <path d="M 710,105 Q 875,20 1030,105" stroke="#4caf50" stroke-width="2.5" fill="none" marker-end="url(#arrowGreen)"/>
        <path d="M 445,128 Q 370,185 308,128" stroke="#3a5fa0" stroke-width="2.5" fill="none" marker-end="url(#arrowBlue1)"/>
        <path d="M 445,128 Q 318,200 203,128" stroke="#6a8fc0" stroke-width="2" fill="none" marker-end="url(#arrowBlue2)"/>
        <path d="M 445,128 Q 512,185 567,128" stroke="#3a5fa0" stroke-width="2.5" fill="none" marker-end="url(#arrowBlue1)"/>
        <path d="M 445,128 Q 568,205 677,128" stroke="#6a8fc0" stroke-width="2" fill="none" marker-end="url(#arrowBlue2)"/>
        <path d="M 445,128 Q 262,215 93,128" stroke="#9ab0d0" stroke-width="1.8" fill="none" marker-end="url(#arrowBlue3)"/>
        <path d="M 445,128 Q 612,215 767,128" stroke="#9ab0d0" stroke-width="1.8" fill="none" marker-end="url(#arrowBlue3)"/>
      </svg>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Get more context for text</div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="font-size:36px; line-height:1.9;">
      <ul style="margin:0 0 8px 0; padding-left:1.1em;">
        <li>Get a more context for: <span style="color:#1a73e8; font-style:italic;">Noa can be <u>annoying</u> but she is a great cat</span></li>
      </ul>
    </div>
    <div style="font-size:36px; margin:2px 0 16px 1.8em; line-height:1;">
      Words <span style="color:#4caf50;">Noa</span>, <span style="color:#4caf50;">is</span> and <span style="color:#4caf50;">cat</span> are "closer" to <span style="color:#4caf50;">she</span>. So, we cannot blindly use proximity.
    </div>
    <div style="font-size:36px; margin:2px 0 16px 1.8em; line-height:1;">
    Think of a way to do this automatically
    </div>
<div style="display:flex; flex-direction:column; align-items:center; margin-top:0px;">
  <img 
    src="media/ppt/media/图片11.png"
    alt="Neural Machine Translation Sequence to Sequence Model"
    style="width:auto; max-width:80%; height:auto; border-radius:12px;"
  >
</div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Review of embedding vectors</div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
<div style="font-size:30px; line-height:1.7;">
  <ul style="margin:0 0 4px 0; padding-left:1.1em;">
    <li>
      Embedding of the word "<span style="color:#4caf50;">king</span>": 
      <span style="color:#4caf50;">\(\boldsymbol{v}_{\text{king}}\)</span> = 
      <span style="display: inline-flex; gap: 0px; vertical-align: middle;">
        <!-- 10 个方框 -->
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
      </span>
      \(\in \mathbb{R}^d\)
    </li>
    <li>
      Embedding of the word "<span style="color:#1a73e8;">queen</span>": 
      <span style="color:#1a73e8;">\(\boldsymbol{v}_{\text{queen}}\)</span> = 
      <span style="display: inline-flex; gap: 0px; vertical-align: middle;">
        <!-- 10 个方框，同上 -->
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
        <span style="display: inline-block; width: 28px; height: 28px; border: 2px solid #555; background: transparent;"></span>
      </span>
      \(\in \mathbb{R}^d\)
    </li>
    <li>Embeddings encode different "meanings"</li>
  </ul>
</div>
    <div style="display:flex; gap:1rem; align-items:flex-start; margin-top:8px;">
      <div style="flex:1.2;">
        <svg viewBox="0 0 580 320" xmlns="http://www.w3.org/2000/svg" style="width:100%; border:none;">
          <defs>
            <marker id="arrPurple" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#8e44ad"/></marker>
            <marker id="arrNavy"   markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1a2e6e"/></marker>
            <marker id="arrBlue"   markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#1a73e8"/></marker>
            <marker id="arrGreen"  markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#4caf50"/></marker>
          </defs>
          <text x="0" y="55" font-size="28" font-family="serif" fill="#4caf50" font-style="italic" font-weight="bold">x</text>
          <text x="18" y="62" font-size="18" font-family="serif" fill="#4caf50">king</text>
          <text x="60" y="55" font-size="28" font-family="sans-serif" fill="#333"> = </text>
          <rect x="88"  y="30" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="126" y="30" width="38" height="34" fill="#8e44ad" stroke="#aaa" stroke-width="1.2"/>
          <rect x="164" y="30" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="202" y="30" width="38" height="34" fill="#1a2e6e" stroke="#aaa" stroke-width="1.2"/>
          <rect x="240" y="30" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="278" y="30" width="38" height="34" fill="#1a73e8" stroke="#aaa" stroke-width="1.2"/>
          <rect x="316" y="30" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="354" y="30" width="38" height="34" fill="#29b6f6" stroke="#aaa" stroke-width="1.2"/>
          <rect x="392" y="30" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="430" y="30" width="38" height="34" fill="#4caf50" stroke="#aaa" stroke-width="1.2"/>
          <text x="472" y="55" font-size="24" font-family="serif" fill="#333">∈ ℝ</text>
          <text x="520" y="45" font-size="16" font-family="serif" fill="#333">d</text>
          <text x="0" y="155" font-size="28" font-family="serif" fill="#1a73e8" font-style="italic" font-weight="bold">x</text>
          <text x="18" y="162" font-size="18" font-family="serif" fill="#1a73e8">queen</text>
          <text x="66" y="155" font-size="28" font-family="sans-serif" fill="#333"> = </text>
          <rect x="88"  y="130" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="126" y="130" width="38" height="34" fill="#8e44ad" stroke="#aaa" stroke-width="1.2"/>
          <rect x="164" y="130" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="202" y="130" width="38" height="34" fill="#1a2e6e" stroke="#aaa" stroke-width="1.2"/>
          <rect x="240" y="130" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="278" y="130" width="38" height="34" fill="#1a73e8" stroke="#aaa" stroke-width="1.2"/>
          <rect x="316" y="130" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="354" y="130" width="38" height="34" fill="#29b6f6" stroke="#aaa" stroke-width="1.2"/>
          <rect x="392" y="130" width="38" height="34" fill="white" stroke="#aaa" stroke-width="1.2"/>
          <rect x="430" y="130" width="38" height="34" fill="#4caf50" stroke="#aaa" stroke-width="1.2"/>
          <text x="472" y="155" font-size="24" font-family="serif" fill="#333">∈ ℝ</text>
          <text x="520" y="145" font-size="16" font-family="serif" fill="#333">d</text>
          <line x1="145" y1="64" x2="145" y2="130" stroke="#8e44ad" stroke-width="1.8" stroke-dasharray="4,3"/>
          <line x1="221" y1="64" x2="221" y2="130" stroke="#1a2e6e" stroke-width="1.8" stroke-dasharray="4,3"/>
          <line x1="297" y1="64" x2="297" y2="130" stroke="#1a73e8" stroke-width="1.8" stroke-dasharray="4,3"/>
          <line x1="373" y1="64" x2="373" y2="130" stroke="#29b6f6" stroke-width="1.8" stroke-dasharray="4,3"/>
          <line x1="449" y1="64" x2="449" y2="130" stroke="#4caf50" stroke-width="1.8" stroke-dasharray="4,3"/>
          <path d="M 145,175 Q 100,210 72,230" stroke="#8e44ad" stroke-width="2" fill="none" marker-end="url(#arrPurple)"/>
          <text x="0" y="250" font-size="22" font-family="sans-serif" fill="#8e44ad">Family</text>
          <path d="M 221,175 Q 200,220 175,240" stroke="#1a2e6e" stroke-width="2" fill="none" marker-end="url(#arrNavy)"/>
          <text x="100" y="270" font-size="22" font-family="sans-serif" fill="#1a2e6e">Royalty</text>
          <path d="M 298,175 Q 265,215 262,245" stroke="#1a73e8" stroke-width="2" fill="none" marker-end="url(#arrNavy)"/>
          <text x="245" y="270" font-size="22" font-family="sans-serif" fill="#1a73e8">Power</text>
          <path d="M 375,175 Q 355,180 360,228" stroke="#1a73e8" stroke-width="2" fill="none" marker-end="url(#arrBlue)"/>
          <text x="330" y="255" font-size="22" font-family="sans-serif" fill="#1a73e8">Gender</text>
          <path d="M 451,175 Q 440,205 468,222" stroke="#4caf50" stroke-width="2" fill="none" marker-end="url(#arrGreen)"/>
          <text x="435" y="250" font-size="22" font-family="sans-serif" fill="#4caf50">Sentiment</text>
          <text x="0" y="310" font-size="30" font-family="sans-serif" fill="red" font-weight="bold">Idea of re-weighing</text>
        </svg>
        <div style="font-size:30px; margin-top:0; padding-left:10px;">
          \(\boldsymbol{W}_{\text{king,queen}} \propto \) <span style="color:#4caf50;">\(\boldsymbol{x}_{\text{king}}\)</span> \(\cdot\) <span style="color:#1a73e8;">\(\boldsymbol{x}_{\text{queen}}\)</span>
        </div>
      </div>
      <div style="flex:0.85; font-size:30px; line-height:2; padding-top:5px;">
        <div style="display:flex; gap:5rem;">
          <div>
            <div style="color:#e59400;">Son</div>
            <div style="color:#e59400;">Daughter</div>
            <div style="color:#e59400;">Cousin</div>
            <div style="color:#e59400;">Land</div>
            <div style="color:#e59400;">Country</div>
            <div style="color:#e59400;">Army</div>
            <div style="color:#e59400;">Own</div>
            <div style="color:#e59400; font-size:22px; margin-top:4px;">Strong relation</div>
          </div>
          <div>
            <div style="color:#aaa;">Dog</div>
            <div style="color:#aaa;">Cat</div>
            <div style="color:#aaa;">Running</div>
            <div style="color:#aaa;">Swimming</div>
            <div style="color:#aaa;">Help</div>
            <div style="color:#aaa;">Nurse</div>
            <div style="color:#aaa;">Computer</div>
            <div style="color:#aaa; font-size:22px; margin-top:4px;">Weak relation</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Explore re-weighing via embedding</div>
  <div class="ppt-line"></div>
  <div style="display: flex; justify-content: center; margin-top: 10px;">
    <img src="media/ppt/media/图片12.png" alt="Re-weighing illustration" style="width: 100%; max-width: 1300px; border: none; box-shadow: none; background: none;">
  </div>

  <!-- 右上角链接保持不变 -->
  <div style="position: absolute; top: 10px; right: 20px; font-size: 18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Explore re-weighing via embedding</div>
  <div class="ppt-line"></div>
  <div style="display: flex; justify-content: center; margin-top: 10px;">
    <img src="media/ppt/media/图片13.png" alt="Re-weighing illustration" style="width: 100%; max-width: 1300px; border: none; box-shadow: none; background: none;">
  </div>

  <!-- 右上角链接保持不变 -->
  <div style="position: absolute; top: 10px; right: 20px; font-size: 18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Self-Attention</div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start;">
      <div style="flex:1.1; font-size:30px; line-height:1.5;">
        <img src="media/ppt/media/图片14.png" alt="Time series prediction chart" style="width:90%; border:none; box-shadow:none; background:none;">
      </div>
      <div style="flex:1; font-size:36px; line-height:1.2; margin-top:50px;">
        <!-- 将所有列表项放在同一个 <ul> 内，便于统一控制间距 -->
        <ul style="margin:0; padding-left:1.1em; list-style-type:disc;">
          <li style="margin-bottom:20px;">Because the word 'river' is here, bank shouldn't refer to money but should refer to the bank of the river, as in the water bank. 
          </li>
            <li style="margin-bottom:20px;">
            The hope is that this <span style="color:red;"><b> attention mechanism</b></span> will be able to correct for that, such that embeddings that come out will have that extra bit of context.
            </li>
        </ul>
      </div>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=tIvKXrEDMhk" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Self-Attention</div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:100%;">
    <img src="media/ppt/media/图片15.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
    <div style="position:absolute; top:2%; right:1%; width:50%; font-size:32px; font-weight:bold; color:red; line-height:1.4;">
      Hope that this new \(\boldsymbol{y}_3\) has more and better context than embedding \(\boldsymbol{v}_3\).
    </div>
    <div style="position:absolute; top:25%; right:5%; width:26%; font-size:28px; line-height:1.3;">
      Similarly, hope that \(\boldsymbol{z}_1, \boldsymbol{z}_2, \boldsymbol{z}_3, \boldsymbol{z}_4\) have more and better context than \(\boldsymbol{x}_1, \boldsymbol{x}_2, \boldsymbol{x}_3, \boldsymbol{x}_4\).
    </div>
    <div style="position:absolute; top:52%; right:5%; width:46%; font-size:28px; line-height:1.3;">
      Calculate the importance of these embeddings with respect to current embedding \(\boldsymbol{x}_3\). A good way is to use softmax <span style="color:red; font-weight:bold;">normalization</span>
    </div>
    <div style="position:absolute; top:78%; right:5%; width:46%; font-size:28px; line-height:1.3;">
      Given "Bank of the river", consider embedding of "<span style="color:purple; font-weight:bold;">the</span>" \(\boldsymbol{x}_3\). The <span style="color:red; font-weight:bold;">dot product</span> of this embedding and other embeddings gives us <b>scores</b>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
  Self-Attention 
  <span style="color:#4caf50; font-size: 0.6em;">Whole block</span>
</div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:95%;">
    <img src="media/ppt/media/图片16.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
    <div style="position:absolute; top:87%; right:5%; width:30%; font-size:26px; line-height:1.3;">
       <span style="color:red; font-weight:bold;">No weights for model to train. How can we introduce weights?
      </span>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
  Self-Attention 
  <span style="color:#4caf50; font-size: 0.6em;">Whole block</span>
</div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:95%;">
    <img src="media/ppt/media/图片17.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
    <div style="position:absolute; top:57%; right:5%; width:30%; font-size:36px; line-height:1.3;">
       Key observation:
       \(\boldsymbol{x}_3\) has been used in three places
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
  Self-Attention 
  <span style="color:#4caf50; font-size: 0.6em;">Adding parameters</span>
</div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:95%;">
    <img src="media/ppt/media/图片18.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
    <div style="position:absolute; top:12%; right:1%; width:38%; font-size:36px; line-height:1;">
      <span style="color:red; font-weight:bold;"> <li> Query:</li> </span> treat vector \(\boldsymbol{x}_3\) as a query and ask this block to get more context for \(\boldsymbol{x}_3\)
    </div>
    <div style="position:absolute; top:52%; right:1%; width:38%; font-size:36px; line-height:1;">
      <span style="color:red; font-weight:bold;"> <li> Key:</li> </span> block will search all contexts. At this moment these \(\boldsymbol{x}_i\) are keys so that we can get scores
    </div>
    <div style="position:absolute; top:80%; right:1%; width:38%; font-size:36px;  line-height:1;">
      <span style="color:red; font-weight:bold;"> <li> Value:</li> </span> Finally, we obtain some values of this query
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Self-Attention <span style="color:#4caf50; font-size: 0.6em;">Key, Value, Query</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start;">
      <div style="flex:1.2; font-size:40px; line-height:2;">
        <ul style="margin:0; padding-left:1.1em;">
          <li><span style="color: black;">A Python dictionary d = {</span><span style="color:#29b6f6;">'a'</span><span style="color: black;">: </span><span style="color:#4caf50;">1</span><span style="color: black;">, </span><span style="color:#29b6f6;">'b'</span><span style="color: black;">: </span><span style="color:#4caf50;">2</span><span style="color: black;">, </span><span style="color:#29b6f6;">'c'</span><span style="color: black;">: </span><span style="color:#4caf50;">3</span><span style="color: black;">}</span></li>
          <li><span style="color: black;"><b>Keys</b> = </span><span style="color:#29b6f6;">{'a', 'b', 'c'}</span></li>
          <li><span style="color: black;"><b>Values</b> = </span><span style="color:#4caf50;">{1, 2, 3}</span></li>
          <li><span style="color: black;">A <b>query</b> d[</span><span style="color:#29b6f6;">'b'</span><span style="color: black;">] = </span><span style="color:#4caf50;">3</span></li>
        </ul>
      </div>
      <div style="flex:0.7; font-size:28px; text-align:center; margin-top:10px;">
        <div style="display:flex; justify-content:space-around; font-size:36px; padding-bottom:8px; border-bottom:2px solid #555; margin-bottom:0;">
          <span style="color:#29b6f6;">Key</span>
          <span style="color:#4caf50;">Value</span>
        </div>
        <div style="display:flex; justify-content:space-around; padding:16px 0; border-bottom:1.5px solid #ccc;">
          <span style="color:#29b6f6;">a</span>
          <span style="color:#4caf50;">1</span>
        </div>
        <div style="display:flex; justify-content:space-around; padding:16px 0; border-bottom:1.5px solid #ccc;">
          <span style="color:#29b6f6;">b</span>
          <span style="color:#4caf50;">2</span>
        </div>
        <div style="display:flex; justify-content:space-around; padding:16px 0; border-bottom:1.5px solid #ccc;">
          <span style="color:#29b6f6;">c</span>
          <span style="color:#4caf50;">3</span>
        </div>
      </div>
    </div>
    <div style="font-size:40px; line-height:1.3; margin-top:56px;">
      <ul style="margin:0; padding-left:1.1em;">
        <li><span style="color: black;">Intuition: Think of our attention mechanism as a softened version of a dictionary where the key, query, and value are all vectors of the same size</span></li>
      </ul>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
  Self-Attention 
</div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:95%;">
    <img src="media/ppt/media/图片19.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
    <div style="position:absolute; top:28%; right:70%; width:25%; font-size:36px; font-weight:bold; line-height:1;">
      <span style="color:green; font-weight:bold;"> \(\boldsymbol{W}^Q\) </span> 
      , <span style="color:purple; font-weight:bold;"> \(\boldsymbol{W}^K\) </span>, <span style="color:red; font-weight:bold;"> \(\boldsymbol{W}^V\) </span> are matrices that can be trained!
    </div>
<div style="position:absolute; top:55%; right:70%; width:25%; font-size:36px; font-weight:bold; line-height:1;">
  We will write 
  <span style="color:green;">\( \boldsymbol{Q} = \boldsymbol{X} \boldsymbol{W}^Q \)</span>
  <span style="color:purple;">\( \boldsymbol{K} = \boldsymbol{X} \boldsymbol{W}^K \)</span>
  <span style="color:red;">\( \boldsymbol{V} = \boldsymbol{X} \boldsymbol{W}^V \)</span>
</div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Self-Attention <span style="color:#4caf50; font-size: 0.6em;">A single block</span></div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:95%;">
    <img src="media/ppt/media/图片20.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
    <div style="position:absolute; top:68%; right:30%; width:30%; font-size:36px; font-weight:bold; line-height:1.3;">
      <span style="color:red; font-weight:bold;">Back propagation for updating \(\boldsymbol{K}\), \(\boldsymbol{Q}\), \(\boldsymbol{V}\) </span> 
    </div>
<div style="position:absolute; top:68%; right:0%; width:25%; font-size:36px; font-weight:bold; line-height:1.3;">
  More and better contextualized embedding
</div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=yGTUuEx3GkA" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Self-Attention <span style="color:#4caf50; font-size:0.6em;">Is one self-attention enough?</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="font-size:36px; line-height:1.8;">
      <ul style="margin:0 0 10px 0; padding-left:1.1em;">
        <li>Take the sentence: "I gave my dog Charlie some food."</li>
        <li>Where should the attention of "gave" go?</li>
      </ul>
    </div>
    <div style="display:flex; justify-content:center; margin:0 0 10px 0;">
      <svg viewBox="0 0 1060 290" xmlns="http://www.w3.org/2000/svg" style="width:100%;">
        <defs>
          <marker id="sa-arrGreen" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L10,4 z" fill="#4caf50"/></marker>
          <marker id="sa-arrRed"   markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L10,4 z" fill="#c0392b"/></marker>
          <marker id="sa-arrBlue"  markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L10,4 z" fill="#1a73e8"/></marker>
        </defs>
        <line x1="315" y1="15" x2="315" y2="68" stroke="#1a73e8" stroke-width="2.8" marker-end="url(#sa-arrBlue)"/>
        <text x="175"  y="108" font-size="36" font-family="sans-serif" fill="#333"    text-anchor="middle">I</text>
        <text x="315"  y="108" font-size="36" font-family="sans-serif" fill="red"     text-anchor="middle" font-weight="bold">gave</text>
        <text x="455"  y="108" font-size="36" font-family="sans-serif" fill="#333"    text-anchor="middle">my</text>
        <text x="590"  y="108" font-size="36" font-family="sans-serif" fill="#333"    text-anchor="middle">dog</text>
        <text x="730"  y="108" font-size="36" font-family="sans-serif" fill="#333"    text-anchor="middle">Charlie</text>
        <text x="880"  y="108" font-size="36" font-family="sans-serif" fill="#333"    text-anchor="middle">some</text>
        <text x="1010" y="108" font-size="36" font-family="sans-serif" fill="#333"    text-anchor="middle">food.</text>
        <path d="M 295,118 Q 230,185 185,128" stroke="#4caf50" stroke-width="2.8" fill="none" marker-end="url(#sa-arrGreen)"/>
        <path d="M 335,118 Q 530,220 720,128" stroke="#4caf50" stroke-width="2.8" fill="none" marker-end="url(#sa-arrGreen)"/>
        <path d="M 330,118 Q 670,265 1000,128" stroke="#c0392b" stroke-width="2.8" fill="none" marker-end="url(#sa-arrRed)"/>
      </svg>
    </div>
    <div style="display:flex; gap:0rem; font-size:36px; line-height:1.3; margin-top:0px;">
      <div style="flex:1; margin-top:-70px; margin-left:50px;">
        <div>Who is doing the giving?</div>
        <div>Who am I giving it to?</div>
        <div>What am I giving?</div>
      </div>
      <div style="flex:1.3; margin-top:-70px; font-size:36px; line-height:1.3;">
        For a single attention, do we have enough parameters to capture these relations?
      </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Multi-attention</div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="font-size:36px; line-height:1.8;">
      <ul style="margin:0 0 10px 0; padding-left:1.1em;">
        <li>Take the sentence: "I gave my dog Charlie some food."</li>
        <li>Where should the attention of "gave" go?</li>
      </ul>
    </div>
    <div style="display:flex; justify-content:center; margin:0 0 10px 0;">
      <svg viewBox="0 0 1060 310" xmlns="http://www.w3.org/2000/svg" style="width:100%;">
        <defs>
          <marker id="ma-arrGreen" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L10,4 z" fill="#4caf50"/></marker>
          <marker id="ma-arrRed"   markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L10,4 z" fill="#c0392b"/></marker>
          <marker id="ma-arrBlue"  markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L10,4 z" fill="#1a73e8"/></marker>
        </defs>
        <line x1="315" y1="15" x2="315" y2="68" stroke="#1a73e8" stroke-width="2.8" marker-end="url(#ma-arrBlue)"/>
        <text x="175"  y="108" font-size="36" font-family="sans-serif" fill="#333"   text-anchor="middle">I</text>
        <text x="315"  y="108" font-size="36" font-family="sans-serif" fill="red"    text-anchor="middle" font-weight="bold">gave</text>
        <text x="455"  y="108" font-size="36" font-family="sans-serif" fill="#333"   text-anchor="middle">my</text>
        <text x="590"  y="108" font-size="36" font-family="sans-serif" fill="#333"   text-anchor="middle">dog</text>
        <text x="730"  y="108" font-size="36" font-family="sans-serif" fill="#333"   text-anchor="middle">Charlie</text>
        <text x="880"  y="108" font-size="36" font-family="sans-serif" fill="#333"   text-anchor="middle">some</text>
        <text x="1010" y="108" font-size="36" font-family="sans-serif" fill="#333"   text-anchor="middle">food.</text>
        <path d="M 295,118 Q 230,185 185,128" stroke="#4caf50" stroke-width="2.8" fill="none" marker-end="url(#ma-arrGreen)"/>
        <text x="118" y="170" font-size="22" font-family="sans-serif" fill="#4caf50" text-anchor="middle">Attention</text>
        <text x="118" y="194" font-size="22" font-family="sans-serif" fill="#4caf50" text-anchor="middle">mechanism 1</text>
        <path d="M 335,118 Q 530,220 720,128" stroke="#4caf50" stroke-width="2.8" fill="none" marker-end="url(#ma-arrGreen)"/>
        <text x="520" y="135" font-size="22" font-family="sans-serif" fill="#4caf50" text-anchor="middle">Attention</text>
        <text x="520" y="159" font-size="22" font-family="sans-serif" fill="#4caf50" text-anchor="middle">mechanism 2</text>
        <path d="M 330,118 Q 670,275 1000,128" stroke="#c0392b" stroke-width="2.8" fill="none" marker-end="url(#ma-arrRed)"/>
        <text x="760" y="215" font-size="22" font-family="sans-serif" fill="#c0392b" text-anchor="middle">Attention</text>
        <text x="760" y="239" font-size="22" font-family="sans-serif" fill="#c0392b" text-anchor="middle">mechanism 3</text>
      </svg>
    </div>
    <div style="display:flex; gap:0rem; font-size:36px; line-height:1.3; margin-top:0px;">
      <div style="flex:1; margin-top:-90px; margin-left:50px;">
        <div>Who is doing the giving?</div>
        <div>Who am I giving it to?</div>
        <div>What am I giving?</div>
      </div>
      <div style="flex:1.3; margin-top:-70px; font-size:36px; line-height:1.4;">
        <div>For a single attention, do we have enough parameters to capture these relations?</div>
        <div style="color:red; font-weight:bold; margin-top:10px;">We can use Multiple attentions!</div>
      </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Multi-attention <span style="color:#4caf50; font-size:0.6em;"> Multi-head attention</span></div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:95%;">
    <img src="media/ppt/media/图片21.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
<div style="position:absolute; top:83%; right:32%; width:35%; font-size:36px; font-weight:bold; line-height:1.3;">
  More and better contextualized embedding
</div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Multi-head attention with layers</div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:95%;">
    <img src="media/ppt/media/图片22.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
  <div style="position:absolute; top:550px; right:150px; font-size:36px;">
    <a href="https://colab.research.google.com/drive/1hXIQ77A4TYS4y3UthWF-Ci7V7vVUoxmQ?usp=sharing" style="color:#1a73e8;">Interactive visualization</a>
  </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Quick recap of self-attention</div>
  <div class="ppt-line"></div>
    <div style="font-size:40px; line-height:1.8;">
      <ul style="margin:0 0 10px 0; padding-left:1.1em;">
        <li><b>Goal:</b> Capture contextual relationships between words in a sequence for various tasks. Components: <b>Queries (𝑸), Keys (𝑲), and Values (𝑽)</b> vectors for each word
        </li>
      </ul>
      </div>
      <div style="font-size:35px; line-height:1.8;">
      <ul style="margin:0 0 10px 0; padding-left:3em;">
        <li>Transform each word into Query, Key, and Value vectors</li>
        <li>Calculate dot products between the Query vector and Key vectors</li>
        <li>Normalize dot products using softmax to get scores (weights)</li>
        <li>Compute weighted sum of Value vectors to create a new representation</li>
      </ul>
    </div>
    <div style="font-size:40px; line-height:1.8;">
      <ul style="margin:0 0 10px 0; padding-left:1.1em;">
        <li><b>Result:</b> Output sequence representation encodes contextual information about its relationship with other words in the input
        </li>
      </ul>
      </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Outline</div>
  <div class="ppt-line"></div>
  <ul class="outline-bullets big">
    <li class="muted">Encoder-decoder model</li>
    <li class="muted">Attention mechanism</li>
    <li class="muted">Self-attention</li>
    <li class="activate">Transformer</li>
  </ul>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer</div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:100%;">
    <img src="media/ppt/media/图片23.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformers <span style="color:#4caf50;">Two building blocks</span></div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:100%;">
    <img src="media/ppt/media/图片24.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Model architecture</span></div>
  <div class="ppt-line"></div>
  <div style="position:relative; width:100%;">
    <img src="media/ppt/media/图片25.png" alt="Self-Attention diagram" style="width:100%; border:none; box-shadow:none; background:none; display:block;">
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Model architecture</span></div>
  <div class="ppt-line"></div>
  <div style="display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:2rem; align-items:flex-start;">
      <div style="flex:1.1; font-size:30px; line-height:1.5;">
        <img src="media/ppt/media/图片26.png" alt="Time series prediction chart" style="width:90%; border:none; box-shadow:none; background:none;">
      </div>
      <div style="flex:1; font-size:30px; line-height:2; margin-top:50px;">
        <!-- 将所有列表项放在同一个 <ul> 内，便于统一控制间距 -->
        <ul style="margin:0; padding-left:1.1em; list-style-type:disc;">
<span style="color:red;"> <b>1. Inputs</span><br>
1. Positional encoding<br>
2. Input/Output embedding<br>
3. Multi-Head Attention<br>
4. Add & Norm<br>
5. Feed Forward<br>
6. Linear<br>
7. Softmax<br>
8. 𝑵
        </ul>
      </div>
    </div>
  </div>
  <div style="position:absolute; top:10px; right:20px; font-size:18px;">
    <a href="https://www.youtube.com/watch?v=tIvKXrEDMhk" style="color:#1a73e8;">Rasa Algorithm Whiteboard 2</a>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
  Transformer
  <span style="font-size: 0.7em; color:#4caf50;">Input</span>
</div>
  <div class="ppt-line"></div>
<div style="font-size:36px; line-height:1.3;margin-left:30px; margin-bottom:10px;">
<li>Transformers typically take sequences of token embeddings as input, which can be <span style="color:red;"> words, subwords, or even characters</span>. These embeddings are obtained from a pre-trained embedding model
  </div>
  
<!-- 视频演示改为图片演示 -->
<div style="display:flex; flex-direction:column; align-items:center; margin-top:20px;">
  <img 
    src="media/ppt/media/图片27.png"
    alt="Neural Machine Translation Sequence to Sequence Model"
    style="width:auto; max-width:100%; height:auto; border-radius:12px;"
  >
</div>

<div style="font-size:36px; line-height:1.3; margin-left:30px; margin-bottom:10px;">
<li>In terms of MT, how should we process the raw text to tokens?
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input (BPE)</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 40px; line-height: 1.8;">
    <ul style="padding-left: 1.2em;">
      <li>
        Instead of
        <ul style="padding-left: 1.2em;">
          <li>white-space segmentation (words tokenization)</li>
          <li>single-character segmentation (character tokenization)</li>
        </ul>
      </li>
      <li style="margin-bottom: 1.2em;"><strong>Use the data</strong> to tell us how to tokenize</li>
      <li style="margin-top: 1.2em;"><strong>Subword tokenization</strong> (because tokens can be parts of words as well as whole words)</li>
    </ul>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input (BPE)</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 35px; line-height: 1.6;">
    <ul style="padding-left: 1.2em;">
      <li style="margin-bottom: 16px;">
        Three common algorithms of subword tokenization:
        <ul style="padding-left: 1.2em; margin-top: 8px;">
          <li style="margin-bottom: 6px;"><strong>Byte-Pair Encoding (BPE)</strong> (Sennrich et al., 2016)</li>
          <li style="margin-bottom: 6px;"><strong>Unigram language modeling tokenization</strong> (Kudo, 2018)</li>
          <li style="margin-bottom: 6px;"><strong>WordPiece</strong> (Schuster and Nakajima, 2012)</li>
        </ul>
      </li>
      <li style="margin-bottom: 16px;">
        All have 2 parts:
        <ul style="padding-left: 1.2em; margin-top: 8px;">
          <li style="margin-bottom: 6px;">A token <strong>learner</strong> that takes a raw training corpus and induces a vocabulary (a set of tokens)</li>
          <li style="margin-bottom: 6px;">A token <strong>segmenter</strong> that takes a raw test sentence and tokenizes it according to that vocabulary</li>
        </ul>
      </li>
    </ul>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input (BPE)</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 35px; line-height: 1.6;">
    <div style="font-weight: bold; margin-bottom: 16px;">Byte Pair Encoding (BPE) token learner</div>
    <ul style="padding-left: 1.2em;">
      <li style="margin-bottom: 12px;">
        Let vocabulary be the set of all individual characters
        <br>
        <span style="display: inline-block; margin-top: 8px; margin-left: 1.2em;">
          \( \{A, B, C, D, \dots, a, b, c, d, \dots\} \)
        </span>
      </li>
      <li style="margin-bottom: 12px;">
        Repeat:
        <ul style="padding-left: 1.2em; margin-top: 8px;">
          <li style="margin-bottom: 6px;">Choose the two symbols that are most frequently adjacent in the training corpus (say 'A', 'B')</li>
          <li style="margin-bottom: 6px;">Add a new merged symbol 'AB' to the vocabulary</li>
          <li style="margin-bottom: 6px;">Replace every adjacent 'A' 'B' in the corpus with 'AB'</li>
        </ul>
      </li>
      <li style="margin-bottom: 12px;">
        Until \( k \) merges have been done
      </li>
    </ul>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input (BPE)</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 37px; line-height: 1.6;">
    <div style="font-weight: bold; margin-bottom: 12px;">BPE token learner</div>
    <ul style="padding-left: 1.2em; margin-bottom: 20px;">
      <li style="margin-bottom: 10px;">
        Original (very fascinating 🙄) corpus:
        <div style="font-family: monospace; margin-top: 6px; margin-left: 1.2em; color: #4897cd; font-weight: bold;">
          low low low low low lowest lowest newer newer newer newer newer newer wider wider wider new new
        </div>
      </li>
      <li style="margin-bottom: 5px;">
        Add end-of-word tokens, resulting in this vocabulary:
      </li>
    </ul>
    <div style="display: flex; gap: 40px; margin-left: 40px;">
      <!-- 左侧：Vocabulary -->
      <div style="flex: 1;">
        <div style="font-weight: bold; margin-bottom: 5px;">Vocabulary</div>
        <div style="font-family: monospace; font-size: 35px;">
          _,&thinsp;d,&thinsp;e,&thinsp;i,&thinsp;l,&thinsp;n,&thinsp;o,&thinsp;r,&thinsp;s,&thinsp;t,&thinsp;w
        </div>
      </div>
      <!-- 右侧：Corpus representation -->
      <div style="flex: 1;">
        <div style="font-weight: bold; margin-bottom: 5px;">Corpus representation</div>
        <div style="font-family: monospace; font-size: 35px; line-height: 1.4;">
          <div>5 l o w _</div>
          <div>2 l o w e s t _</div>
          <div>6 n e w e r _</div>
          <div>3 w i d e r _</div>
          <div>2 n e w _</div>
        </div>
      </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Input (BPE)</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 4rem; font-size: 36px; line-height: 1.3;">
    <!-- 左侧内容 -->
    <div style="flex: 1; list-style: disc; margin-left: 50px;">
      <div style="margin-bottom: 12px;"><li>BPE token learner</li></div>
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 12px; margin-left: 30px;">Vocabulary</div>
      <div style="font-family: monospace; margin-bottom: 70px; font-size: 32px; margin-left: 30px;">
        _,&thinsp;d,&thinsp;e,&thinsp;i,&thinsp;l,&thinsp;n,&thinsp;o,&thinsp;r,&thinsp;s,&thinsp;t,&thinsp;w
      </div>
      <div style="margin-bottom: 5px; font-size: 35px;">
        Merge <span style="color: #4897cd; font-weight: bold;">e r</span>  to <span style="color: #4897cd; font-weight: bold;">er</span>
      </div>
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 12px; margin-left: 30px;">Vocabulary</div>
      <div style="font-family: monospace; font-size: 32px; margin-left: 30px;">
        _,&thinsp;d,&thinsp;e,&thinsp;i,&thinsp;l,&thinsp;n,&thinsp;o,&thinsp;r,&thinsp;s,&thinsp;t,&thinsp;w,&thinsp;<span style="color: #e53935; font-weight: bold;">er</span>
      </div>
    </div>
    <div style="flex: 1;">
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 15px; margin-left: 15px;">Corpus representation</div>
      <div style="font-family: monospace; margin-bottom: 40px; font-size: 35px; line-height: 1.4; margin-left: 15px">
        <div>5 l o w _</div>
        <div>2 l o w e s t _</div>
        <div>6 n e w e r _</div>
        <div>3 w i d e r _</div>
        <div>2 n e w _</div>
      </div>
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 15px; margin-left: 15px;">Corpus representation</div>
      <div style="font-family: monospace; font-size: 35px; line-height: 1.4;margin-left: 15px">
        <div>5 l o w _</div>
        <div>2 l o w e s t _</div>
        <div>6 n e w <span style="color: #e53935; font-weight: bold;">er</span> _</div>
        <div>3 w i d <span style="color: #e53935; font-weight: bold;">er</span> _</div>
        <div>2 n e w _</div>
      </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Input (BPE)</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 4rem; font-size: 36px; line-height: 1.3;">
    <!-- 左侧内容 -->
    <div style="flex: 1; list-style: disc; margin-left: 50px;">
      <div style="margin-bottom: 12px;"><li>BPE token learner</li></div>
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 12px; margin-left: 30px;">Vocabulary</div>
      <div style="font-family: monospace; margin-bottom: 70px; font-size: 32px; margin-left: 30px;">
        _,&thinsp;d,&thinsp;e,&thinsp;i,&thinsp;l,&thinsp;n,&thinsp;o,&thinsp;r,&thinsp;s,&thinsp;t,&thinsp;w,&thinsp;er
      </div>
      <div style="margin-bottom: 5px; font-size: 35px;">
        Merge <span style="color: #4897cd; font-weight: bold;">er _</span>  to <span style="color: #4897cd; font-weight: bold;">er_</span>
      </div>
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 12px; margin-left: 30px;">Vocabulary</div>
      <div style="font-family: monospace; font-size: 32px; margin-left: 30px;">
        _,&thinsp;d,&thinsp;e,&thinsp;i,&thinsp;l,&thinsp;n,&thinsp;o,&thinsp;r,&thinsp;s,&thinsp;t,&thinsp;w,&thinsp;er,&thinsp;<span style="color: #e53935; font-weight: bold;">er_</span>
      </div>
    </div>
    <div style="flex: 1;">
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 15px; margin-left: 15px;">Corpus representation</div>
      <div style="font-family: monospace; margin-bottom: 40px; font-size: 35px; line-height: 1.4; margin-left: 15px">
        <div>5 l o w _</div>
        <div>2 l o w e s t _</div>
        <div>6 n e w er _</div>
        <div>3 w i d er _</div>
        <div>2 n e w _</div>
      </div>
      <div style="font-weight: bold; font-size: 40px; margin-bottom: 15px; margin-left: 15px;">Corpus representation</div>
      <div style="font-family: monospace; font-size: 35px; line-height: 1.4;margin-left: 15px">
        <div>5 l o w _</div>
        <div>2 l o w e s t _</div>
        <div>6 n e w <span style="color: #e53935; font-weight: bold;">er_</span></div>
        <div>3 w i d <span style="color: #e53935; font-weight: bold;">er_</span></div>
        <div>2 n e w _</div>
      </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input (BPE)</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 40px; list-style: disc; line-height: 1.5; margin-left: 30px;">
    <p style="margin-bottom: 16px;"><li>BPE token learner</li></p>
    <p style="margin-bottom: 12px;"><li>The next merges are:</li></p>
    <!-- 左右两列布局 -->
    <div style="display: flex; gap: 40px; margin-top: 10px;">
      <!-- 左侧：Merge 列表 -->
      <div style="flex: 1;">
        <div style="font-weight: bold; margin-bottom: 8px;">Merge</div>
        <ul style="font-weight: bold; margin: 0; font-size: 32px;list-style-type: none;">
          <li style="margin-bottom: 6px;">(ne, w)</li>
          <li style="margin-bottom: 6px;">(l, o)</li>
          <li style="margin-bottom: 6px;">(lo, w)</li>
          <li style="margin-bottom: 6px;">(new, er_)</li>
          <li style="margin-bottom: 6px;">(low, er_)</li>
        </ul>
      </div>
      <!-- 右侧：Current Vocabulary 列表 -->
      <div style="flex: 1;">
        <div style="font-weight: bold; margin-bottom: 8px; margin-left: -200px;">Current Vocabulary</div>
        <div style="font-family: monospace; font-size: 32px; line-height: 1.4; margin-left: -480px;">
          _, d, e, i, l, n, o, r, s, t, w, er, <span style="color: #e53935; font-weight: bold;">er_, ne, new</span><br>
          _, d, e, i, l, n, o, r, s, t, h, w, er, <span style="color: #e53935; font-weight: bold;">er_, ne, new, lo</span><br>
          _, d, e, i, l, n, o, r, s, t, w, er, <span style="color: #e53935; font-weight: bold;">er_, ne, new, low</span><br>
          _, d, e, i, l, n, o, r, s, t_<br>
          _, d, e, i, l, n, o, r, s, t, w, er, <span style="color: #e53935; font-weight: bold;">er_, ne, new, low, newer_</span><br>
          _, d, e, i, l, n, o, r, s, t, w, er, <span style="color: #e53935; font-weight: bold;">er_, ne, new, low, newer_, low_</span>
        </div>
      </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input (BPE)</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 35px; line-height: 1.5; list-style: disc; margin-left: 30px;">
    <p style="margin-bottom: 16px;"><li>BPE token <strong>segmenter</strong> algorithm</li></p>
    <p style="margin-bottom: 12px;">On the test data, run each merge learned from the training data:</p>
    <ul style="padding-left: 1.8em; margin-bottom: 16px;">
      <li style="margin-bottom: 6px;">Greedily</li>
      <li style="margin-bottom: 6px;">In the order we learned them</li>
      <li style="margin-bottom: 6px;">(test frequencies don't play a role)</li>
    </ul>
    <p style="margin-bottom: 16px;">
      So: merge every <span style="color: #4897cd; font-weight: bold;">e r</span> to <span style="color: #4897cd; font-weight: bold;">er</span>, then merge <span style="color: #4897cd; font-weight: bold;">e r _</span> to <span style="color: #4897cd; font-weight: bold;">er_</span>, etc.
    </p>
    <p style="margin-bottom: 12px; font-weight: bold;"><li>Result:</li></p>
    <ul style="padding-left: 1.8em;">
      <li style="margin-bottom: 8px;">Test set "n e w e r _" would be tokenized as a full word</li>
      <li style="margin-bottom: 8px;">Test set "l o w e r _" would be two tokens: "low er_"</li>
    </ul>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 3rem; align-items: flex-start;">
    <div style="flex: 1.2; margin-left: 10px;">
      <img src="media/ppt/media/figure1.png" alt="Transformer Model Architecture" style="width: 100%; max-width: 650px; border: none; box-shadow: none; background: none; margin-top: -18px;">
    </div>
    <div style="flex: 1; font-size: 36px; font-weight: bold; line-height: 1.5; padding-top: 20px;">
      <div style="margin-bottom: 12px;">1. Inputs</div>
      <div style="margin-bottom: 12px; color: #e53935;">2. Positional encoding</div>
      <div style="margin-bottom: 12px;">3. Input/Output embedding</div>
      <div style="margin-bottom: 12px;">4. Multi-Head Attention</div>
      <div style="margin-bottom: 12px;">5. Add & Norm</div>
      <div style="margin-bottom: 12px;">6. Feed Forward</div>
      <div style="margin-bottom: 12px;">7. Linear</div>
      <div style="margin-bottom: 12px;">8. Softmax</div>
      <div>9. \(N\)</div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Positional encoding</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 2rem; align-items: flex-start;">
    <div style="flex: 1;">
      <ul style="list-style: disc; padding-left: 1.1em; font-size: 32px; line-height: 1.4; margin-bottom: 5px;">
        <li>Use sine and cosine functions of different frequencies:</li>
      </ul>
    <div style="font-size: 28px; line-height: 1.4; text-align: center; margin: 5px 0;">
      \[
      PE(pos, 2i) = \sin\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
      \]
      \[
      PE(pos, 2i+1) = \cos\left(\frac{pos}{10000^{2i/d_{\text{model}}}}\right)
      \]
    </div>
      <div style="margin-top: 5px; margin-left: 10px;">
        <img src="media/ppt/media/figure2.png" alt="Positional Encoding Sine Cosine Waves" style="width: 100%; max-width: 1000px; border: none; box-shadow: none; background: none;">
      </div>
    </div>
    <div style="flex: 1; display: flex; justify-content: center; align-items: flex-start;">
      <img src="media/ppt/media/figure3.png" alt="Positional Encoding Python Code" style="width: 100%; max-width: 600px; border: none; box-shadow: none; background: none;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 2rem; align-items: flex-start;">
    <div style="flex: 1;">
      <ul style="list-style: disc; padding-left: 1.1em; font-size: 35px; line-height: 1.4; margin-bottom: 5px;">
        <li style="margin-bottom: 30px;">How this combination of sines and cosines could ever represent a position/order?</li>
        <li style="margin-bottom: 30px;">It is actually quite simple, suppose you want to represent a number in binary format, how will that be?</li>
        <li style="margin-bottom: 30px;">You can spot the rate of change between different bits. The lowest bit is alternating on every number, the second-lowest bit is rotating on every two numbers, and so on.</li>
      </ul>
    </div>
    <div style="flex: 1; font-weight: bold; margin-top: 130px;  margin-left: 55px;">
        <div style="font-family: monospace; font-size: 40px; line-height: 1;">
          0:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">0</span>&thinsp;8 :&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">0</span><br>
          1:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">1</span>&thinsp;9 :&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">1</span><br>
          2:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">0</span>&thinsp;10:&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">0</span><br>
          3:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">1</span>&thinsp;11:&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">0</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">1</span><br>
          4:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">0</span>&thinsp;12:&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">0</span><br>
          5:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">1</span>&thinsp;13:&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">0</span> <span style="color: #e53935; font-weight: bold;">1</span><br>
          6:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">0</span>&thinsp;14:&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">0</span><br>
          7:&ensp;<span style="color: #e5b636; font-weight: bold;">0</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">1</span>&thinsp;15:&ensp;<span style="color: #e5b636; font-weight: bold;">1</span> <span style="color: #038c1e; font-weight: bold;">1</span> <span style="color: #1c23d7; font-weight: bold;">1</span> <span style="color: #e53935; font-weight: bold;">1</span><br>
        </div>
      </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Positional encoding</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; align-items: flex-start;">
    <!-- 左侧文字和公式 -->
    <div style="flex: 1; font-size: 40px; line-height: 1.5;  margin-left: 100px;">
      <img src="media/ppt/media/figure5.png" alt="Positional encoding visualization" style="max-width: 200%; height: 400px; border: 1px solid #ffffff; border-radius: 4px;">
      <p style="text-align: left;">
      \( \omega_k = \frac{1}{10000^{2k/d}} \)
      </p>
      <p style="margin-top: 20px;">\( t \) is position index</p>
    </div>
    <!-- 右侧图片 -->
    <div style="flex: 1; text-align: center;">
      <img src="media/ppt/media/figure4.png" alt="Positional encoding visualization" style="margin-top:100px; margin-left: -300px; max-width: 500%; height: 400px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Positional encoding</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 30px; align-items: flex-start;">
    <!-- 左侧内容 -->
    <div style="flex: 1.2; font-size: 32px; line-height: 1.4; margin-top: -15px;">
      <p style="margin-bottom: 10px;">
        <span style="color: #e53935;">• Is Positional Encoding necessary?</span>
        <em>Transformer Language Models without Positional Encodings Still Learn Positional Information</em>
      </p>
      <!-- 论文图片 -->
      <div style="margin-top: -30px; text-align: center;">
        <img src="media/ppt/media/figure7.png" alt="Paper screenshot" style="max-width: 100%; border: 1px solid #ffffff; border-radius: 4px;">
      </div>
      <!-- 作者信息 -->
      <div style="font-size: 20px; margin: 15px 0; line-height: 1.3; color: #333; margin-top: -25px;">
        <a href="https://github.com/adihaviv/NoPos" style="color: #1a73e8; margin-left: 240px;">https://github.com/adihaviv/NoPos</a>
      </div>
      <!-- 方法列表 -->
      <div style="margin-top: 20px;">
        <p style="margin-top: -15px;">• <strong>Learned</strong>: Used by MLMs, GPT-3</p>
        <p style="margin-top: -15px;">• <strong>Sinusoidal</strong>: Used by Transformer</p>
        <p style="margin-top: -15px;">• <strong>ALiBi</strong>: Linear Biases (Press et al., 2022, ICLR)</p>
        <p style="margin-top: -15px;">• <strong>NoPos</strong>: Without Positional encoding information</p>
      </div>
      <div style="font-size: 25px;">RoPE&emsp;<a href="https://arxiv.org/pdf/2104.09864" target="_blank">RoFormer: Enhanced Transformer with Rotary Position Embedding</a></div>
    </div>
    <!-- 右侧图片 -->
    <div style="flex: 0.8; text-align: center;">
      <img src="media/ppt/media/figure6.png" alt="Positional encoding comparison" style="max-width: 100%; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 3rem; align-items: flex-start;">
    <div style="flex: 1.2; margin-left: 10px;">
      <img src="media/ppt/media/figure47.png" alt="Transformer Model Architecture" style="width: 100%; max-width: 645px; border: none; box-shadow: none; background: none; margin-top: -18px;">
    </div>
    <div style="flex: 1; font-size: 36px; font-weight: bold; line-height: 1.5; padding-top: 20px;">
      <div style="margin-bottom: 12px;">1. Inputs</div>
      <div style="margin-bottom: 12px;">2. Positional encoding</div>
      <div style="margin-bottom: 12px; color: #e53935;">3. Input/Output embedding</div>
      <div style="margin-bottom: 12px;">4. Multi-Head Attention</div>
      <div style="margin-bottom: 12px;">5. Add & Norm</div>
      <div style="margin-bottom: 12px;">6. Feed Forward</div>
      <div style="margin-bottom: 12px;">7. Linear</div>
      <div style="margin-bottom: 12px;">8. Softmax</div>
      <div>9. \(N\)</div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input Embedding</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; align-items: flex-start;">
    <!-- 左侧文字内容 -->
    <div style="flex: 1.2; list-style: disc; font-size: 35px; line-height: 1.5;">
      <li style="margin-bottom: 16px;">We have static embeddings</li>
      <ul style="padding-left: 1.5em; margin-bottom: 24px;">
        <li>word2vec/GloVe/fastText</li>
      </ul>
    </div>
    <!-- 右侧代码图片 -->
    <div style="flex: 0.9; text-align: center;">
      <img src="media/ppt/media/figure8.png" alt="Embeddings class code" style="max-width: 100%; max-width: 640px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
  <div style="list-style: disc; font-size: 35px; margin-left: 30px; margin-top: -40px;">
    <li>Ways to have embeddings</li>
    <li style="font-size: 30px; margin-left: 60px;">initialize it with pre-trained embeddings and keep it fixed</li>
    <li style="font-size: 30px; margin-left: 60px;">initialize it randomly, or with pre-trained embeddings, but keep it trainable. Word embeddings will get refined and modified throughout training</li>
    <li style="margin-top: 20px;">The Transformer uses a random initialization of the weight matrix and refines these weights during training</li>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Input Output Embedding</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 30px; align-items: stretch;">
    <div style="flex: 1; margin-top: 30px;">
    <img src="media/ppt/media/figure44.png" alt="Transformer Model Architecture2" style="width: 200%; max-width: 600px; margin-top: 35px; border: none; box-shadow: none; background: none;">
    </div>
    <div style="flex: 1; margin-top: 30px;">
      <img src="media/ppt/media/figure45.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 560px; border: none; box-shadow: none; background: none;">
    </div>
  </div>
  <div style="margin-left: 30px; font-size: 35px;">During training, the decoder doesn’t generate tokens from scratch; it’s given the previous gold tokens (a process called teacher forcing). So at step t, it’s trying to predict the next word given all the previous ones.</div>
  <img src="media/ppt/media/figure46.png" alt="Transformer Model Architecture2" style="width: 100%; margin-left: 150px; max-width: 900px; border: none; box-shadow: none; background: none;">
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 3rem; align-items: flex-start;">
    <div style="flex: 1.2; margin-left: 10px;">
      <img src="media/ppt/media/figure43.png" alt="Transformer Model Architecture" style="width: 100%; max-width: 650px; border: none; box-shadow: none; background: none; margin-top: -18px;">
    </div>
    <div style="flex: 1; font-size: 36px; font-weight: bold; line-height: 1.5; padding-top: 20px;">
      <div style="margin-bottom: 12px;">1. Inputs</div>
      <div style="margin-bottom: 12px;">2. Positional encoding</div>
      <div style="margin-bottom: 12px;">3. Input/Output embedding</div>
      <div style="margin-bottom: 12px; color: #e53935;">4. Multi-Head Attention</div>
      <div style="margin-bottom: 12px;">5. Add & Norm</div>
      <div style="margin-bottom: 12px;">6. Feed Forward</div>
      <div style="margin-bottom: 12px;">7. Linear</div>
      <div style="margin-bottom: 12px;">8. Softmax</div>
      <div>9. \(N\)</div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Multi-head Attention</span></div>
  <div class="ppt-line"></div>
  
  <!-- 左右布局：左侧图片，右侧文字内容 -->
  <div style="display: flex; gap: 40px; align-items: flex-start;">
    <!-- 左侧：Scaled Dot-Product Attention 图示 -->
    <div style="flex: 1; text-align: left;">
      <img src="media/ppt/media/figure9.png" alt="Scaled Dot-Product Attention" style="max-width: 270%; height: 640px; border: 1px solid #ffffff; border-radius: 4px; margin-top: 25px;">
    </div>
    <!-- 右侧：公式与解释文字 -->
    <div style="flex: 1; font-size: 30px; line-height: 1.3; margin-left: 400px; list-style: disc;">
      <li style="margin-bottom: 20px; margin-left: 50px;">
        What is the <span style="color: #e5b636;">scale</span> in scaled dot-product attention?
      </li>
      <div style="font-size: 22px; margin: 20px 0;">
        \[
        \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\color[rgb]{0.898,0.714,0.212}{\sqrt{d_k}}}\right)\cdot V
        \]
      </div>
      <li style="margin-left: 50px;">
        Assume that \( u \) and \( v \) are \( d_k \)-dimensional vectors whose components are independent random variables with mean 0 and variance 1.
      </li>
      <li style="margin-left: 50px; margin-top: 20px;">
        Their dot product,
        \(
        u \cdot v = \sum_{i=1}^{d_k} u_i \cdot v_i
        \)
        has mean 0 and variance \( d_k \). <strong><span style="color: #e53935;">Since we would prefer these values to have variance 1, we divide by \(\sqrt{d_k}\)</span>.</strong>
      </li>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Multi-head Attention</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; align-items: stretch;">
    <div style="flex: 1; text-align: center;">
      <img src="media/ppt/media/figure10.png" alt="Scaled Dot-Product Attention" style="max-width: 250%; height: 650px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
    <div style="flex: 1; display: flex; margin-left: 400px; flex-direction: column; gap: 30px;">
        <div style="font-size: 29px; line-height: 1.3; list-style: disc; margin-top: 50px; margin-left: 30px;">
          <li style="margin-bottom: 12px;"><strong>What is the <span style="color: #e53935;">Mask (opt.)</span> in scaled dot-product attention?</strong></li>
          <li>To prevent positions from attending to subsequent positions. Ensure that the predictions for position \( i \) can depend only on known outputs at positions less than \( i \).</li>
        </div>
        <img src="media/ppt/media/figure11.png" alt="Mask chart" style="max-width: 85%; height: 280px; margin-top: -20px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Multi-head Attention</span></div>
  <div class="ppt-line"></div>
  <div style="font-weight: bold; font-size: 40px; margin-left: 30px;">Attention Visualizations</div>
  <div style="display: flex; flex-direction: column; align-items: center; gap: 20px;">
    <!-- 图片 -->
    <div style="width: 100%; text-align: center;">
      <img src="media/ppt/media/figure12.png" alt="Attention visualization" style="max-width: 100%; height: 430px; border: 1px solid #ffffff; border-radius: 4px; margin-top: -10px;">
    </div>
    <div style="font-size: 30px; line-height: 1.4; text-align: left; width: 100%; margin-top: -65px;">
      <p style="margin-bottom: 12px;">
        An example of the attention mechanism following long-distance dependencies in the encoder self-attention in layer 5 of 6. Many of the attention heads attend to a distant dependency of the verb ‘making’, completing the phrase ‘making…more difficult’. Attentions here shown only for the word ‘making’. Different colors represent different heads. Best viewed in color.
      </p>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Multi-head Attention</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; align-items: stretch;">
    <div style="flex: 1; text-align: left;">
      <div style="font-weight: bold; font-size: 40px; margin-left: 30px;">Attention Visualizations</div>
      <img src="media/ppt/media/figure13.png" alt="Attention Visualization1" style="max-width: 250%; height: 500px; margin-left: 30px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
    <div style="flex: 1; display: flex; margin-left: -200px; flex-direction: column; gap: 30px;">
      <img src="media/ppt/media/figure14.png" alt="Attention Visualization2" style="max-width: 55%; height: 500px; margin-top: -15px; margin-left: 150px; border: 1px solid #ffffff; border-radius: 4px;">
        <div style="font-size: 28px; line-height: 1.1; margin-top: -40px; margin-left: -30px;">Many of the attention heads exhibit behavior that seems related to the structure of the sentence. We give two such examples above, from two different heads from the encoder self-attention at layer 5 of 6. The heads clearly learned to perform different tasks.
        </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Multi-head Attention</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px;">
  <div style="flex: 1; font-size: 40px; font-weight: bold; margin-bottom: 20px;">Is multi-head attention useful?</div>
  <div style="flex: 1; font-size: 22px; margin-left: -190px; line-height: 1.2;">Even if models have been trained using multiple heads, in practice, a large percentage of attention heads can be removed at test time without significantly impacting performance. In fact, some layers can even be reduced to a single head
  .</div>
  </div>
  <!-- 大表格图片 -->
  <div style="text-align: center;">
    <img src="media/ppt/media/figure16.png" alt="Multi-head attention table" style="max-width: 100%; height: 250px; border: 1px solid #ffffff; border-radius: 4px; margin-top: -5px;">
  </div>
  <div style="display: flex; gap: 30px; align-items: flex-start; font-size: 20px; flex-wrap: wrap; margin-top: -45px;">
    <div style="flex: 1; min-width: 200px;">
      <img src="media/ppt/media/figure15.png" alt="Authors" style="max-width: 90%; border: 1px solid #ffffff; border-radius: 4px; margin-left: 20px;">
      <a href="https://arxiv.org/abs/1905.10650" target="_blank" style="font-size: 30px; margin-left: 130px; margin-top: -30px;">NeurIPS, 2019</a>
    </div>
    <div style="flex: 1; min-width: 200px;">
      <img src="media/ppt/media/figure17.png" alt="Table 2" style="max-width: 90%; border: 1px solid #ffffff; border-radius: 4px;">
      <p style="margin-top: -30px; margin-left: -45px;"><strong>Table 2:</strong> Best delta BLEU by layer when only one head is kept in the WMT model. Underlined numbers indicate that the change is statistically significant with \( p < 0.01 \).</p>
    </div>
    <div style="flex: 1; min-width: 200px;">
      <img src="media/ppt/media/figure18.png" alt="Table 3" style="max-width: 90%; border: 1px solid #ffffff; border-radius: 4px; margin-left: -20px;">
      <p style="margin-top: -30px; margin-left: -25px;"><strong>Table 3:</strong> Best delta accuracy by layer when only one head is kept in the BERT model. None of these results are statistically significant with \( p < 0.01 \).</p>
    </div>
  </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 3rem; align-items: flex-start;">
    <div style="flex: 1.2; margin-left: 10px;">
      <img src="media/ppt/media/figure42.png" alt="Transformer Model Architecture" style="width: 100%; max-width: 650px; margin-top: -18px; border: none; box-shadow: none; background: none;">
    </div>
    <div style="flex: 1; font-size: 36px; font-weight: bold; line-height: 1.5; padding-top: 20px;">
      <div style="margin-bottom: 12px;">1. Inputs</div>
      <div style="margin-bottom: 12px;">2. Positional encoding</div>
      <div style="margin-bottom: 12px;">3. Input/Output embedding</div>
      <div style="margin-bottom: 12px;">4. Multi-Head Attention</div>
      <div style="margin-bottom: 12px; color: #e53935;">5. Add & Norm</div>
      <div style="margin-bottom: 12px;">6. Feed Forward</div>
      <div style="margin-bottom: 12px;">7. Linear</div>
      <div style="margin-bottom: 12px;">8. Softmax</div>
      <div>9. \( N \)</div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Add & Norm</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; align-items: stretch;">
    <div style="flex: 1; text-align: left; list-style: disc;">
      <li style="font-size: 40px; margin-left: 30px; line-height: 1.2; margin-top: 50px; margin-right: 100px;">Add & Norm improves training, without making changes to the core of the model.</li>
      <li style="font-size: 40px; margin-left: 30px; margin-top: 20px; margin-right: 100px;">It has two steps:</li>
      <li style="font-size: 30px; margin-left: 60px; margin-top: 20px; margin-right: 100px;">The <strong>add step</strong> is a residual connection, the technique proposed in <span style="color: #787878;">Deep Residual Learning for Image Recognition, CVPR, 2015</span>. It means that we take sum together the output of a layer with the input. It is one of the solutions for vanishing gradient problem.</li>
    </div>
    <div style="flex: 1; display: flex; margin-left: -200px; flex-direction: column; gap: 30px;">
      <img src="media/ppt/media/figure19.png" alt="Attention Visualization2" style="max-width: 80%; height: 320px; margin-left: 100px; margin-top: -15px; border: 1px solid #ffffff; border-radius: 4px;">
      <img src="media/ppt/media/figure20.png" alt="Attention Visualization2" style="max-width: 80%; height: 320px; margin-left: 100px; margin-top: -40px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Add & Norm</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; align-items: stretch;">
    <div style="flex: 1; text-align: left; list-style: disc;">
      <li style="font-size: 40px; margin-left: 30px; line-height: 1.2; margin-top: 50px; margin-right: 100px;">Add & Norm improves training, without making changes to the core of the model.</li>
      <li style="font-size: 40px; margin-left: 30px; margin-top: 20px; margin-right: 100px;">It has two steps:</li>
      <li style="font-size: 30px; margin-left: 60px; margin-top: 20px; margin-right: 100px;">The <strong>norm step</strong> is about layer normalization (<span style="color: #787878;">Ba et al, 2016</span>), it is another way of normalization. It is one of the many computational tricks to make life easier for training the model, hence improve the performance and training time.
      </li>
    </div>
    <div style="flex: 1; display: flex; margin-left: -200px; flex-direction: column; gap: 30px;">
      <img src="media/ppt/media/figure21.png" alt="Attention Visualization2" style="max-width: 80%; height: 200px; margin-left: 100px; margin-top: -15px; border: 1px solid #ffffff; border-radius: 4px; margin-top: 25px;">
      <img src="media/ppt/media/figure22.png" alt="Attention Visualization2" style="max-width: 80%; height: 320px; margin-left: 100px; margin-top: -40px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 3rem; align-items: flex-start;">
    <div style="flex: 1.2; margin-left: 10px;">
      <img src="media/ppt/media/figure41.png" alt="Transformer Model Architecture" style="width: 100%; max-width: 650px; margin-top: -18px; border: none; box-shadow: none; background: none;">
    </div>
    <div style="flex: 1; font-size: 36px; font-weight: bold; line-height: 1.5; padding-top: 20px;">
      <div style="margin-bottom: 12px;">1. Inputs</div>
      <div style="margin-bottom: 12px;">2. Positional encoding</div>
      <div style="margin-bottom: 12px;">3. Input/Output embedding</div>
      <div style="margin-bottom: 12px;">4. Multi-Head Attention</div>
      <div style="margin-bottom: 12px;">5. Add & Norm</div>
      <div style="margin-bottom: 12px; color: #e53935;">6. Feed Forward</div>
      <div style="margin-bottom: 12px;">7. Linear</div>
      <div style="margin-bottom: 12px;">8. Softmax</div>
      <div>9. \( N \)</div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Feed forward</span></div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; align-items: stretch;">
    <div style="flex: 1; text-align: left; list-style: disc;">
      <li style="font-size: 40px; margin-left: 30px; line-height: 1.1; margin-top: 50px; margin-right: 100px; margin-bottom: 60px; line-height: 1.2;">Each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically. This consists of two linear transformations with a ReLU activation in between.</li>
      <div style="font-size: 30px; margin-right: 40px;">
      \[
        FFN(x)=\text{max}(0,xW_1+b_1)W_2+b_2
      \]
      </div>
    </div>
    <div style="flex: 1; display: flex; margin-left: -200px; flex-direction: column; gap: 30px;">
      <img src="media/ppt/media/figure23.png" alt="Attention Visualization2" style="max-width: 83%; height: 320px; margin-left: 130px; margin-top: 100px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 3rem; align-items: flex-start;">
    <div style="flex: 1.2; margin-left: 10px;">
      <img src="media/ppt/media/figure40.png" alt="Transformer Model Architecture" style="width: 100%; max-width: 650px; margin-top: -18px; border: none; box-shadow: none; background: none;">
    </div>
    <div style="flex: 1; font-size: 36px; font-weight: bold; line-height: 1.5; padding-top: 20px;">
      <div style="margin-bottom: 12px;">1. Inputs</div>
      <div style="margin-bottom: 12px;">2. Positional encoding</div>
      <div style="margin-bottom: 12px;">3. Input/Output embedding</div>
      <div style="margin-bottom: 12px;">4. Multi-Head Attention</div>
      <div style="margin-bottom: 12px;">5. Add & Norm</div>
      <div style="margin-bottom: 12px;">6. Feed Forward</div>
      <div style="margin-bottom: 12px; color: #e53935;">7. Linear</div>
      <div style="margin-bottom: 12px; color: #e53935;">8. Softmax</div>
      <div>9. \( N \)</div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Model architecture</span>
  </div>
  <div class="ppt-line"></div>
  <img src="media/ppt/media/figure24.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 1250px; margin-left: 30px; margin-top: -10px; border: none; box-shadow: none; background: none;">
</section>

---

<section class="ppt">
  <div class="ppt-title">Transformer <span style="color:#4caf50;">Two MT tasks</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 40px; list-style: disc;">
      <li style="margin-left: 30px;">Machine translation</li>
      <li style="font-size: 37px; margin-left: 60px; line-height: 1; margin-top: 30px;"><strong>English-German:</strong> trained on the standard WMT 2014 English-German dataset consisting of about 4.5 million sentence pairs. Sentences were encoded using byte-pair encoding, which has a shared source target vocabulary of about 37000 tokens.</li>
      <li style="font-size: 37px; margin-left: 60px; line-height: 1; margin-top: 25px;"><strong>English-French:</strong> we used the significantly larger WMT 2014 English-French dataset consisting of 36M sentences and split tokens into a 32000 word-piece vocabulary.</li>
      <li style="margin-left: 30px; margin-top: 30px;">Sentence pairs were batched together by approximate sequence length. Each training batch contained a set of sentence pairs containing approximately 25000 source tokens and 25000 target tokens.</li>
    </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Illustrated Transformer via MT</div>
  <div class="ppt-line"></div>
  <div style="list-style: disc; font-size: 40px;">
    <li style="margin-left: 30px;"><div>The encoding component is a stack of six <span style="color: #4897cd;">encoders</span>. </div>
    <div>The decoding component is a stack of six <span style="color: #4897cd;">decoders</span>.</div>
    </li>
  </div>
  <div style="display: flex; gap: 30px; align-items: stretch;">
    <div style="flex: 1;">
      <img src="media/ppt/media/figure25.png" alt="Attention Visualization2" style="max-width: 100%; height: 250px; margin-left: 75px; margin-top: 50px; border: 1px solid #ffffff; border-radius: 4px;">
      <img src="media/ppt/media/figure26.png" alt="Attention Visualization2" style="max-width: 90%; height: 200px; margin-left: 50px; margin-top: -40px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
    <div style="flex: 1;">
      <img src="media/ppt/media/figure27.png" alt="Attention Visualization2" style="max-width: 100%; height: 510px; margin-top: -15px; margin-left: -20px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer </span> 
    <span style="color: #4caf50;">Two MT tasks</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 30px; align-items: stretch;">
    <div style="flex: 1;">
      <img src="media/ppt/media/figure28.png" alt="Attention Visualization2" style="max-width: 100%; height: 380px; margin-right: 25px; margin-top: 70px; border: 1px solid #ffffff; border-radius: 4px;">
      <div style="font-size: 25px; margin-left: 30px; margin-right: 30px;">BLEU scores (higher is better) of single models on the standard WMT newstest2014 <span style="color: #4897cd;">English to German</span> translation benchmark.</div>
    </div>
    <div style="flex: 1;">
      <img src="media/ppt/media/figure29.png" alt="Attention Visualization2" style="max-width: 100%; height: 380px; margin-top: 70px; margin-left: 25px; border: 1px solid #ffffff; border-radius: 4px;">
      <div style="font-size: 25px; margin-left: 30px; margin-right: 30px;">BLEU scores (higher is better) of single models on the standard WMT newstest2014 <span style="color: #4897cd;">English to French</span> translation benchmark.</div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer </span> 
    <span style="color: #4caf50;">Results</span>
  </div>
  <div class="ppt-line"></div>
  <img src="media/ppt/media/figure30.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 1150px; margin-left: 100px; border: none; box-shadow: none; background: none;">
  <div style="list-style: disc; font-size: 30px;">
  <li style="font-size: 35px; margin-left: 80px; margin-top: -15px; margin-right: 80px;">Compared with ConS2S, Transformer big not only provides better BLEU of EN-FR but also with 50 times faster.</li>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer </span> 
    <span style="color: #4caf50;">Model parameters</span>
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 30px; align-items: stretch;">
    <div style="flex: 1; list-style: disc; font-size: 37px; margin-left: 30px;">
      <li style="margin-top: 10px;">\(N\): number of encoder and decoder layers</li>
      <li style="margin-top: 10px;">\(d_{\text{model}}\)dimension of outputs of sub-layers and embedding layers</li>
      <li style="margin-top: 10px;">\(d_{ff}\)dimension of inner layer</li>
      <li style="margin-top: 10px;">\(h\)number of heads in multi-head attention layer</li>
      <li style="margin-top: 10px;">\(d_k\)dimension of queries and keys</li>
      <li style="margin-top: 10px;">\(d_v\)dimension of values</li>
      <li style="margin-top: 10px;">\(P_{\text{drop}}\)dropout rate</li>
      <li style="margin-top: 10px;">\(\epsilon_{\text{ls}}\)Label smoothing value</li>
    </div>
    <div style="flex: 1;">
      <div style="font-size: 37px;">
      \[
        d_k=d_v=\dfrac{d_{\text{model}}}{h}=64
      \]
      <div style="font-size: 40px; margin-left: 30px;"><strong>Transformer base</strong></div>
      <div style="margin-left: 30px;">\(N\)=6&ensp;\(d_{\text{model}}\)=512&ensp;\(d_{ff}\)=2048&ensp;\(h\)=8&ensp;\(d_k\)=64&ensp;\(d_v\)=64&ensp;\(P_{\text{drop}}\)=0.1&ensp;\(\epsilon_{\text{ls}}\)=0.1</div>
      <div style="font-size: 40px; margin-left: 30px; margin-top: 30px;"><strong>Transformer big</strong></div>
      <div style="margin-left: 30px;">\(N\)=6&ensp;\(d_{\text{model}}\)=1024&ensp;\(d_{ff}\)=4096&ensp;\(h\)=16&ensp;\(d_k\)=64&ensp;\(d_v\)=64&ensp;\(P_{\text{drop}}\)=0.3&ensp;\(\epsilon_{\text{ls}}\)=0.1</div>
      </div>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title"><span style="color: #e53935;">Quiz (15 minutes)</span></div>
  <div class="ppt-line"></div>
  <div style="font-size: 35px; list-style: disc;">
      <li style="font-size: 40px; margin-left: 30px;">Consider a Transformer-based model, which contains only the encoder block of the original transformer architecture. Specifically,</li>
      <li style="margin-left: 60px; margin-top: 20px;">Number of layers: \(N\)=12</li>
      <li style="margin-left: 60px; margin-top: 20px;">Model dimension (embedding dimension): \(d\)=768</li>
      <li style="margin-left: 60px; margin-top: 20px;">Number of heads: \(H\)=12</li>
      <li style="margin-left: 60px; margin-top: 20px;">Vocabulary size: \(V\)=30522</li>
      <li style="margin-left: 60px; margin-top: 20px;">Attention dimension \(k\) is set to: \(k\)=\(d/h\)</li>
      <li style="margin-left: 60px; margin-top: 20px;">FFN dimension is set to: \(m=4\cdot d\)</li>
      <li style="font-size: 40px; margin-left: 30px;">Question: How many parameters in this model?</li>
    </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">Results</span>
  </div>
  <div class="ppt-line"></div>
  <img src="media/ppt/media/figure31.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 1000px; margin-left: 170px; margin-top: -10px; border: none; box-shadow: none; background: none;">
</section>

---


<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">English Constituency Parsing</span>
  </div>
  <div class="ppt-line"></div>
  <div style="list-style: disc; font-size: 42px; margin-bottom: 60px; margin-left: 30px;">
    <li>To evaluate if the Transformer can generalize to other tasks we performed experiments on English constituency parsing.</li>
  </div>
  <div style="display: flex; gap: 30px; align-items: stretch;">
    <div style="flex: 1;">
      <div style="list-style: disc; font-size: 42px; margin-left: 30px; margin-right: 60px;">
        <li>We trained a 4-layer transformer on the Wall Street Journal (WSJ) portion of the Penn Treebank, about 40K training sentences.</li>
      </div>
    </div>
    <div style="flex: 1;">
      <img src="media/ppt/media/figure32.png" alt="Attention Visualization2" style="max-width: 100%; height: 380px; margin-top: 20px; border: 1px solid #ffffff; border-radius: 4px;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Transformer</span> 
    <span style="color: #4caf50;">English Constituency Parsing</span>
  </div>
  <div class="ppt-line"></div>
  <img src="media/ppt/media/figure33.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 1250px; margin-left: 55px; margin-top: 20px; border: none; box-shadow: none; background: none;">
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Improving on quadratic self-attention cost</span> 
  </div>
  <div class="ppt-line"></div>
  <div style="font-size: 35px; margin-left: 20px;">For one, we replace dot-product attention by one that uses locality-sensitive hashing, changing its complexity from \(O(n^2)\) to \(O(n\log⁡n)\), where \(n\) is the length of the sequence. Furthermore, we use reversible residual layers instead of the standard residuals, which allows storing activations only once in the training process instead of L times, where L is the number of layers.</div>
  <div style="display: flex; gap: 30px; align-items: stretch;">
    <div style="flex: 1; margin-right: -550px;">
      <img src="media/ppt/media/figure34.png" alt="Transformer Model Architecture2" style="width: 200%; max-width: 900px; margin-left: 40px; margin-top: 20px; border: none; box-shadow: none; background: none;">
    </div>
    <div style="flex: 1; margin-left: 1010px;">
      <img src="media/ppt/media/figure35.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 420px; margin-top: 120px; border: none; box-shadow: none; background: none;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Improving on quadratic self-attention cost</span> 
  </div>
  <div class="ppt-line"></div>
  <div style="font-size: 35px; margin-left: 20px;">In this paper, we demonstrate that the self-attention mechanism can be approximated by a low-rank matrix. We further exploit this finding to propose a new self-attention mechanism, which reduces the overall self-attention complexity from \(O(n^2)\) to \(O(n^1)\) in both time and space.
  </div>
  <img src="media/ppt/media/figure36.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 900px; margin-top: -10px; margin-left: 230px; border: none; box-shadow: none; background: none;">
  <img src="media/ppt/media/figure39.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 600px; margin-left: 360px; margin-top: -10px; border: none; box-shadow: none; background: none;">
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Do Transformer Modifications Transfer?</span> 
  </div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 30px; align-items: stretch;">
    <div style="flex: 1; font-size: 40px; margin-top: 30px; list-style: disc; margin-left: 30px;">
      <li style="margin-right: 300px;">“Surprisingly, we find that most modifications do not meaningfully improve performance.”</li>
    <img src="media/ppt/media/figure37.png" alt="Transformer Model Architecture2" style="width: 200%; max-width: 450px; margin-top: 35px; border: none; box-shadow: none; background: none;">
    <div><a style="font-size: 25px; margin-left: 160px; margin-top: 30px;" href="https://arxiv.org/pdf/2102.11972" target="_blank">EMNLP,2021</a></div>
    </div>
    <div style="flex: 1; margin-left: -300px;">
      <img src="media/ppt/media/figure38.png" alt="Transformer Model Architecture2" style="width: 100%; max-width: 800px; margin-top: 120px; border: none; box-shadow: none; background: none;">
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">Compared with RNNs</div>
  <div class="ppt-line"></div>
  <div style="display: flex; gap: 40px; margin-top: 20px;">
    <!-- 左侧：Challenges with RNNs -->
    <div style="flex: 1; background: #f5f5f5; border-radius: 12px; margin-top: 30px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
      <div style="font-size: 40px; font-weight: bold; margin-bottom: 20px;">Challenges with RNNs</div>
      <ul style="font-size: 35px; line-height: 1.5; margin: 0; padding-left: 1.2em;">
        <li style="margin-bottom: 12px;">Long range dependencies</li>
        <li style="margin-bottom: 12px;">Gradient vanishing and explosion</li>
        <li style="margin-bottom: 12px;">Large # of training steps</li>
        <li style="margin-bottom: 12px;">Recurrence prevents parallel computation</li>
      </ul>
    </div>
    <!-- 右侧：Transformer Networks -->
    <div style="flex: 1; background: #f5f5f5; border-radius: 12px; margin-top: 30px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
      <div style="font-size: 40px; font-weight: bold; margin-bottom: 20px;">Transformer Networks</div>
      <ul style="font-size: 35px; line-height: 1.5; margin: 0; padding-left: 1.2em;">
        <li style="margin-bottom: 12px;">Facilitate long range dependencies</li>
        <li style="margin-bottom: 12px;">No gradient vanishing and explosion</li>
        <li style="margin-bottom: 12px;">Fewer training steps</li>
        <li style="margin-bottom: 12px;">No recurrence that facilitate parallel computation</li>
      </ul>
    </div>
  </div>
</section>

---

<section class="ppt">
  <div class="ppt-title">
    <span style="color: var(--fudan-blue);">Useful Resources</span> 
  </div>
  <div class="ppt-line"></div>
  <div style="list-style: disc; font-size: 25px; line-height: 1;">
    <div?>Materials used in this lecture are mainly from online, I list as follows:</div>
    <li style="font-size: 25px; margin-left: 30px;">Annotated-transformer with code: <a style="font-size: 22px; " href="http://nlp.seas.harvard.edu/annotated-transformer/" target="_blank">http://nlp.seas.harvard.edu/annotated-transformer/ </a></li>
    <li style="font-size: 25px; margin-left: 30px;">Great articles made by Jay Alammar</li>
    <li style="font-size: 25px; margin-left: 60px;">Encoder and decoder: <a style="font-size: 22px;" href="https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/" target="_blank">https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/ </a></li>
    <li style="font-size: 25px; margin-left: 60px;">The Illustrated Transformer: <a style="font-size: 22px;" href="https://jalammar.github.io/illustrated-transformer/" target="_blank">https://jalammar.github.io/illustrated-transformer/ </a></li>
    <li style="font-size: 25px; margin-left: 30px;">A series great video by Rasa </li>
    <li style="font-size: 25px; margin-left: 60px;">1 Self-attention: <a style="font-size: 22px;" href="https://www.youtube.com/watch?v=yGTUuEx3GkA" target="_blank">https://www.youtube.com/watch?v=yGTUuEx3GkA </a></li>
    <li style="font-size: 25px; margin-left: 60px;">2 Keys, Values, and Queries: <a style="font-size: 22px;" href="https://www.youtube.com/watch?v=tIvKXrEDMhk" target="_blank">https://www.youtube.com/watch?v=tIvKXrEDMhk </a></li>
    <li style="font-size: 25px; margin-left: 60px;">3 Multi-head attention: <a style="font-size: 22px;" href="https://www.youtube.com/watch?v=23XUv0T9L5c" target="_blank">https://www.youtube.com/watch?v=23XUv0T9L5c </a></li>
    <li style="font-size: 25px; margin-left: 60px;">4 Transformer architecture: <a style="font-size: 22px;" href="https://www.youtube.com/watch?v=EXNBy8G43MM" target="_blank">https://www.youtube.com/watch?v=EXNBy8G43MM </a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://cs.uwaterloo.ca/~ppoupart/teaching/cs480-spring19/schedule.html" target="_blank">https://cs.uwaterloo.ca/~ppoupart/teaching/cs480-spring19/schedule.html </a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://primo.ai/index.php?title=Attention" target="_blank">https://primo.ai/index.php?title=Attention </a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://jalammar.github.io/illustrated-transformer/" target="_blank">https://jalammar.github.io/illustrated-transformer/ </a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://www.youtube.com/watch?v=yGTUuEx3GkA&list=PLYlEnMRwvpF96pIbA6N6wynSgym3OnFAS" target="_blank">https://www.youtube.com/watch?v=yGTUuEx3GkA&list=PLYlEnMRwvpF96pIbA6N6wynSgym3OnFAS </a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html" target="_blank">https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html </a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://koaning.io/" target="_blank">https://koaning.io/ </a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://colah.github.io/posts/2015-08-Understanding-LSTMs/" target="_blank">https://colah.github.io/posts/2015-08-Understanding-LSTMs/</a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="http://nlp.seas.harvard.edu/annotated-transformer/" target="_blank">http://nlp.seas.harvard.edu/annotated-transformer/</a></li>
    <li style="font-size: 25px; margin-left: 30px;"><a style="font-size: 25px;" href="https://people.cs.umass.edu/~miyyer/cs685_f22/slides/04-attention.pdf" target="_blank">https://people.cs.umass.edu/~miyyer/cs685_f22/slides/04-attention.pdf</a></li>
  </div>
</section>