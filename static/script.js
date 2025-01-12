document.getElementById("healthForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const symptoms = Array.from(
    document.querySelectorAll('input[type="checkbox"]:checked')
  ).map((checkbox) => checkbox.value);

  const duration = document.querySelector('input[name="duration"]:checked')?.value;
  const ageGroup = document.getElementById("ageGroup").value;
  const adviceType = Array.from(
    document.querySelectorAll('input[type="checkbox"][value]:checked')
  ).map((checkbox) => checkbox.value);
  const detailedSymptoms = document.getElementById("detailedSymptoms").value;

  const responseDiv = document.getElementById("result");

  if (symptoms.length === 0) {
    responseDiv.textContent = "Molimo izaberite barem jedan simptom.";
    responseDiv.style.color = "red";
    return;
  }

  responseDiv.innerHTML = "Generišem savete... <div class='spinner'></div>";

  try {
    const response = await fetch("/check-symptoms", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms, duration, ageGroup, adviceType, detailedSymptoms }),
    });

    if (!response.ok) throw new Error("Greška u komunikaciji sa serverom.");

    const data = await response.json();
    responseDiv.innerHTML = `<pre>${data.advice}</pre>`;
  } catch (error) {
    responseDiv.textContent = `Greška: ${error.message}`;
    responseDiv.style.color = "red";
  }
});
