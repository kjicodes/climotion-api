const exerciseTypeSelect = document.getElementById("exercise-type")
const targetGroupContainer = document.getElementById("target-group-container")
const expertDifficultyOption = document.getElementById("expert-option")

function toggleTargetGroup() {
    const value = exerciseTypeSelect.value;

    targetGroupContainer.style.display = (value === "cardio") ? "none" : "block";
    expertDifficultyOption.style.display = (value === "stretching") ? "none" : "";

}

exerciseTypeSelect.addEventListener("change", toggleTargetGroup);
toggleTargetGroup();