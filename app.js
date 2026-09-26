const task =
    document.getElementById("task");

const level =
    document.getElementById("level");

const weeksWrap =
    document.getElementById("weeks-wrap");

const weeks =
    document.getElementById("weeks");

const input =
    document.getElementById("input-text");

const button =
    document.getElementById("submit-btn");

const resultCard =
    document.getElementById("result-card");

const result =
    document.getElementById("result");

const source =
    document.getElementById("source");

const errorBox =
    document.getElementById("error");


task.addEventListener(
    "change",
    () => {

        weeksWrap.classList.toggle(
            "hidden",
            task.value !== "learn"
        );


        const placeholders = {

            qa:
                "Example: Why does the sky appear blue?",

            explain:
                "Example: Explain the Pythagorean theorem with a simple example.",

            quiz:
                "Paste a topic or educational passage to generate 3 MCQs.",

            summarize:
                "Paste a long educational passage to summarize.",

            learn:
                "Example: SQL database development",
        };


        input.placeholder =
            placeholders[task.value];
    }
);


function showError(message) {

    errorBox.textContent =
        message;

    errorBox.classList.remove(
        "hidden"
    );
}


function escapeHtml(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );
}


function renderQuiz(
    questions
) {

    result.innerHTML =
        questions
            .map(
                (
                    question,
                    index
                ) => `

                <div class="quiz-question">

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(
                            question.question
                        )}
                    </h3>

                    ${question.options
                        .map(
                            (
                                option,
                                optionIndex
                            ) => `

                            <label
                                class="quiz-option"
                            >

                                <input
                                    type="radio"
                                    name="q-${index}"
                                    value="${escapeHtml(
                                        option
                                    )}"
                                >

                                ${String.fromCharCode(
                                    65 + optionIndex
                                )}.

                                ${escapeHtml(
                                    option
                                )}

                            </label>

                        `
                        )
                        .join("")}

                    <button
                        type="button"
                        data-question="${index}"
                    >
                        Check Answer
                    </button>

                    <div
                        id="feedback-${index}"
                        class="quiz-feedback"
                    ></div>

                </div>
            `
            )
            .join("");


    questions.forEach(
        (
            question,
            index
        ) => {

            const checkButton =
                document.querySelector(
                    `[data-question="${index}"]`
                );


            checkButton.addEventListener(
                "click",
                () => {

                    const selected =
                        document.querySelector(
                            `input[name="q-${index}"]:checked`
                        );


                    const feedback =
                        document.getElementById(
                            `feedback-${index}`
                        );


                    if (!selected) {

                        feedback.textContent =
                            "Choose an option first.";

                        return;
                    }


                    if (
                        selected.value ===
                        question.correct_answer
                    ) {

                        feedback.textContent =
                            `Correct. ${question.explanation}`;

                    } else {

                        feedback.textContent =
                            `Not quite. Correct answer: ${question.correct_answer}. ${question.explanation}`;
                    }
                }
            );
        }
    );
}


async function run() {

    errorBox.classList.add(
        "hidden"
    );


    const text =
        input.value.trim();


    if (!text) {

        showError(
            "Please enter a question or study material."
        );

        return;
    }


    const endpoints = {

        qa:
            "/qa",

        explain:
            "/explain",

        quiz:
            "/quiz",

        summarize:
            "/summarize",

        learn:
            "/learn/recommendations",
    };


    const payload = {

        text:
            text,

        level:
            level.value,
    };


    if (
        task.value ===
        "learn"
    ) {

        payload.weeks =
            Number(weeks.value);
    }


    button.disabled =
        true;

    button.textContent =
        "Thinking...";

    resultCard.classList.add(
        "hidden"
    );


    try {

        const response =
            await fetch(
                endpoints[task.value],
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body:
                        JSON.stringify(
                            payload
                        ),
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "The server returned an error."
            );
        }


        resultCard.classList.remove(
            "hidden"
        );


        source.textContent =
            data.source || "";


        if (
            task.value ===
            "quiz"
        ) {

            renderQuiz(
                data.questions
            );

        } else {

            const value =
                data.answer ||
                data.result ||
                data.summary ||
                data.recommendations;


            result.innerHTML =
                `<div class="answer">${escapeHtml(
                    value
                )}</div>`;
        }


        resultCard.scrollIntoView(
            {
                behavior: "smooth",
                block: "start",
            }
        );


    } catch (error) {

        showError(
            error.message ||
            "Something went wrong."
        );

    } finally {

        button.disabled =
            false;

        button.textContent =
            "Run EduGenie";
    }
}


button.addEventListener(
    "click",
    run
);