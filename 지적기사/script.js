// Auth Check: Redirect to login if not logged in
if (sessionStorage.getItem('isLoggedIn') !== 'true') {
    window.location.href = '../index.html';
}

let allQuestions = [];
let currentQuiz = [];
let currentIndex = 0;
let score = 0;
let timer = null;
let timeLeft = 60;
let currentMode = 'study'; // 'study' or 'exam'
let selectedSource = '기출'; // '기출' or 'all'

// Initialize questions from loaded script
function initQuiz() {
    // Compat: Map 'questions' to 'questionData'
    if (typeof questions !== 'undefined' && typeof questionData === 'undefined') {
        window.questionData = questions;
    }

    if (typeof questionData !== 'undefined') {
        allQuestions = questionData;
        console.log("Loaded questions:", allQuestions.length);
        const countElem = document.getElementById('total-q-count');
        if (countElem) countElem.innerText = allQuestions.length + " 문항";
        if (allQuestions.length > 0) {
            console.log("Example Q:", allQuestions[0]);
        }
    } else {
        console.error("questions.js failed to load.");
        alert("데이터 파일을 불러오지 못했습니다. 새로고침을 해주세요.");
    }
}

window.onload = initQuiz;

function showLanding() {
    document.getElementById('quiz').classList.add('hidden');
    document.getElementById('result').classList.add('hidden');
    document.getElementById('landing').classList.remove('hidden');
}

function setSource(src) {
    selectedSource = src;
    document.getElementById('src-official').classList.toggle('active', src === '기출');
    document.getElementById('src-all').classList.toggle('active', src === 'all');
}

function startQuiz(subject, mode) {
    currentMode = mode;
    console.log("Starting Quiz. Subject:", subject, "Mode:", mode);

    // Filter questions by subject
    // Note: Data subject in generated questions.js is exact match usually.
    let filtered = allQuestions.filter(q => q.subject && q.subject.includes(subject));

    // Optional: Filter by source if needed.
    // For now, since data is segregated by folder, we might not need strict source filtering
    // unless 'selectedSource' logic is desired.
    // current dataset source format: "지적기사 (2022-03-05)"

    /* 
    if (selectedSource === '기출') {
         // Implement if needed
    }
    */

    console.log("Filtered questions:", filtered.length);

    if (filtered.length === 0) {
        alert(`'${subject}' 과목의 문항이 없습니다.\n전체 모드로 시도하시거나 데이터를 확인해주세요.`);
        return;
    }

    if (mode === 'exam') {
        // --- Mock Exam: Random 20 ---
        currentQuiz = filtered.sort(() => 0.5 - Math.random()).slice(0, 20);
    } else {
        // --- Study Mode: All questions shuffled ---
        currentQuiz = [...filtered].sort(() => 0.5 - Math.random());
    }

    currentIndex = 0;
    score = 0;

    document.getElementById('landing').classList.add('hidden');
    document.getElementById('quiz').classList.remove('hidden');

    showQuestion();
}

function showQuestion() {
    if (currentIndex >= currentQuiz.length) {
        showResult();
        return;
    }

    const q = currentQuiz[currentIndex];

    // Header Info
    document.getElementById('curr-subject').innerText = q.subject;
    document.getElementById('curr-num').innerText = "Q" + (currentIndex + 1); // No 'num' field in new data
    document.getElementById('q-text').innerText = q.text;

    // Date Info extraction
    const dateElem = document.getElementById('q-date');
    if (dateElem) {
        dateElem.innerText = q.date || q.source || "";
    }

    // Progress
    const progress = (currentIndex / currentQuiz.length) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
    document.getElementById('q-counter').innerText = `${currentIndex + 1} / ${currentQuiz.length}`;

    // Image
    const imgContainer = document.getElementById('q-image');
    // New data uses 'local_images' array
    if (q.local_images && q.local_images.length > 0) {
        // Use the first image. Path is relative e.g. "images/file.gif"
        imgContainer.innerHTML = `<img src="${q.local_images[0]}" alt="Question Image" onerror="this.style.display='none'">`;
        imgContainer.classList.remove('hidden');
    } else {
        imgContainer.classList.add('hidden');
    }

    // Options
    const optionsContainer = document.getElementById('options');
    optionsContainer.innerHTML = '';
    q.options.forEach((opt, idx) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn glass';
        btn.innerHTML = `<span class="opt-num">${idx + 1}</span> ${opt}`;
        btn.onclick = () => checkAnswer(idx + 1);
        optionsContainer.appendChild(btn);
    });

    // Reset UI
    document.getElementById('explanation').classList.add('hidden');
    document.getElementById('next-btn').classList.add('hidden');

    // Timer (Only in Exam Mode)
    clearInterval(timer);
    if (currentMode === 'exam') {
        document.getElementById('timer').classList.remove('hidden');
        startQuestionTimer();
    } else {
        document.getElementById('timer').classList.add('hidden');
    }
}

function startQuestionTimer() {
    timeLeft = 60;
    updateTimerDisplay();
    timer = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();
        if (timeLeft <= 0) {
            clearInterval(timer);
            handleTimeout();
        }
    }, 1000);
}

function updateTimerDisplay() {
    const min = Math.floor(timeLeft / 60);
    const sec = timeLeft % 60;
    const timerElem = document.getElementById('timer');
    timerElem.innerText = `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;

    if (timeLeft < 10) {
        timerElem.style.color = '#ef4444';
    } else {
        timerElem.style.color = 'var(--admin-primary)';
    }
}

function handleTimeout() {
    alert("시간이 초과되었습니다!");
    checkAnswer(-1, true);
}

function checkAnswer(selectedIdx, isTimeout = false) {
    if (timer) clearInterval(timer);

    const q = currentQuiz[currentIndex];
    const correctAns = parseInt(q.answer);

    const isCorrect = selectedIdx === correctAns;

    const options = document.querySelectorAll('.option-btn');
    options.forEach((btn, idx) => {
        btn.disabled = true;

        if (idx + 1 === correctAns) {
            btn.classList.add('correct');
        } else if (idx + 1 === selectedIdx) {
            btn.classList.add('wrong');
        }
    });

    if (isCorrect) score++;

    // Show Explanation
    const expDiv = document.getElementById('explanation');
    // New data might not have explanation field populated yet, fallback text
    expDiv.querySelector('#exp-text').innerHTML = q.explanation || "해설이 준비중입니다.";
    expDiv.classList.remove('hidden');

    // Show Next Button
    const nextBtn = document.getElementById('next-btn');
    nextBtn.classList.remove('hidden');

    // Auto-scroll
    setTimeout(() => {
        nextBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);

    if (currentMode === 'exam' && isTimeout) {
        setTimeout(nextQuestion, 2000);
    }
}

function nextQuestion() {
    currentIndex++;
    showQuestion();
}

function showResult() {
    document.getElementById('quiz').classList.add('hidden');
    document.getElementById('result').classList.remove('hidden');

    const finalScore = currentQuiz.length > 0 ? Math.round((score / currentQuiz.length) * 100) : 0;
    document.getElementById('final-score').innerText = finalScore;
    document.getElementById('correct-count').innerText = score;
    document.getElementById('total-questions').innerText = currentQuiz.length;
}

function restartQuiz() {
    showLanding();
}
