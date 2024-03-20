document.addEventListener('DOMContentLoaded', function () {
    var quizButtonElement = document.getElementById('answer-button')
    var titleText = document.getElementById("video-name").innerText


    const queryString = window.location.search
    const queryParams = new URLSearchParams(queryString)
    const topicSlug = queryParams.get('topic')

    const questionApiPath = window.location.origin + "/kafka/quiz/questions?topic=" + topicSlug
    const topicApiPath = window.location.origin + "/kafka/quiz/info?topic=" + topicSlug
    var questions = []
    var correct_answers = {}
    var userAnswers = []

    fetch(topicApiPath)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            let topic = data["course_name"]
            document.getElementById("video-name").innerText = document.getElementById("video-name").innerText + " " + topic
            console.log(topic)
        })
        .catch(error => {
            console.error('Error:', error);
        });

    fetch(questionApiPath)
        .then(response => response.json())
        .then(data => {
            correct_answers = data.questions

            for (const [question, answer] of Object.entries(data.questions)) {
                questions.push(question)
                console.log(question)
                document.getElementById("quiz-question").innerText = questions[0]
            }

        })
        .catch(error => {
            console.error('Error:', error);
        });






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
            let payload = {}
            for (let i = 0; i < questions.length; i++) {
                payload[questions[i]] = userAnswers[i]
            }

            let formData = new FormData()
            formData.append('questions_answers', JSON.stringify(payload))
            formData.append('topic', topicSlug)

            fetch('/kafka/quiz/evaluate/', {
                method: 'POST',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: formData
            })
                .then(response => {
                    if (response.ok) {
                        return response.json(); // Parse response as JSON
                    } else {
                        throw new Error('Failed to submit answers');
                    }
                })
                .then(data => {
                    console.log('Answers submitted successfully');
                    console.log(data);

                    const ogContainer = document.getElementById("finished-pair-container");

                    console.log(ogContainer);

                    for (const [question, similarity] of Object.entries(data.similarities)) {
                        console.log(question)
                        let correct_answer = correct_answers[question]

                        const clonedContainer = ogContainer.cloneNode(true);
                        // clonedContainer.style.display = "block";
                        clonedContainer.querySelector("#quiz-done-question").innerText = question;
                        clonedContainer.querySelector("#quiz-done-correct-answer").innerText = correct_answer;
                        clonedContainer.querySelector("#quiz-done-user-answer").innerText = payload[question];
                        clonedContainer.querySelector("#similarity").innerText = Math.floor(similarity * 1000) / 10 + "%";
                        ogContainer.parentElement.appendChild(clonedContainer);
                        // console.log(question);
                        // console.log(similarity);
                        // console.log("lorem");
                    }

                    const result_title = document.getElementById("score-title")

                    result_title.textContent = "Celkový výsledek: " + (Math.floor(data.result * 1000) / 10) + "%"
                })
                .catch(error => {
                    console.error('Error:', error);
                });

            document.getElementById("question-container").style.display = "none"
            document.getElementById("user-answer-container").style.display = "none"

            document.getElementById("video-name").innerText = "Dokončil jsi " + document.getElementById("video-name").innerText;

        }
    }

    quizButtonElement.addEventListener('click', function () {
        var answerInputElement = document.getElementById('answer-input')
        var answer = answerInputElement.value
        checkAnswer(answer)
        console.log(answer)
    })
})

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}