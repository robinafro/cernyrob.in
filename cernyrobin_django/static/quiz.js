document.addEventListener('DOMContentLoaded', function () {
    var quizButtonElement = document.getElementById('answer-button')
    var titleText = document.getElementById("video-name").innerText
    

    const queryString = window.location.search
    const queryParams = new URLSearchParams(queryString)
    const topicSlug = queryParams.get('topic')

    const questionApiPath = window.location.origin + "/quiz/questions?topic=" + topicSlug
    const topicApiPath = window.location.origin + "/quiz/info?topic=" + topicSlug


    fetch(questionApiPath)
        .then(response => response.json())
        .then(data => {
           let qaPairs = data
        })
        .catch(error => {
            console.error('Error:', error);
        });

    fetch(topicApiPath)
        .then(response => response.json())
        .then(data => {
           let topic = data.name
        })
        .catch(error => {
            console.error('Error:', error);
        });





    let questions = [
        'kdy vznikl unix timestamp',
        'kdo udělal linux',
        'kdo udělal gnu',
    ]
    let userAnswers = []

    let currentQuestionIndex = 0

    function displayQuestion() {
        var questionElement = document.getElementById('quiz-question')
        questionElement.textContent = questions[currentQuestionIndex]
    }

    function checkAnswer(answer) {
        userAnswers.push(answer)
        currentQuestionIndex++
        if (currentQuestionIndex < questions.length) {
            displayQuestion()
            document.getElementById('answer-input').value = ""
        } else {
            console.log(userAnswers)
            document.getElementById("question-container").style.display = "none"
            document.getElementById("user-answer-container").style.display = "none"

            document.getElementById("video-name").innerText = "Dokončil jsi " + titleText;

        }
    }

    quizButtonElement.addEventListener('click', function () {
        var answerInputElement = document.getElementById('answer-input')
        var answer = answerInputElement.value
        checkAnswer(answer)
        console.log(answer)
    })
})
