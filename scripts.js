let calculationType = "";

function setCalculationType(type) {
  console.log(`Setting calculation type to: ${type}`);
  calculationType = type;
  document.getElementById("step1").style.display = "none";
  document.getElementById("loanForm").style.display = "flex";
  if (type === "monthlyPayment") {
    document.getElementById("term").style.display = "block";
    document.getElementById("termLabel").style.display = "block";
    document.getElementById("monthlyPayment").style.display = "none";
    document.getElementById("monthlyPaymentLabel").style.display = "none";
  } else if (type === "term" || type === "endDate") {
    document.getElementById("term").style.display = "none";
    document.getElementById("termLabel").style.display = "none";
    document.getElementById("monthlyPayment").style.display = "block";
    document.getElementById("monthlyPaymentLabel").style.display = "block";
  }
}

function calculateLoan() {
  const amount = parseFloat(document.getElementById("amount").value);
  const interestRate =
    parseFloat(document.getElementById("interestRate").value) / 100 / 12;
  const term = parseInt(document.getElementById("term").value);
  const monthlyPayment = parseFloat(
    document.getElementById("monthlyPayment").value
  );
  const startDate = new Date(document.getElementById("startDate").value);

  console.log(
    `amount: ${amount}, interestRate: ${interestRate}, term: ${term}, monthlyPayment: ${monthlyPayment}, startDate: ${startDate}`
  );

  let resultText = "";

  if (calculationType === "monthlyPayment") {
    if (isNaN(amount) || isNaN(interestRate) || isNaN(term)) {
      resultText = "Por favor, asegúrese de que todos los valores son válidos.";
    } else if (interestRate === 0) {
      const calculatedMonthlyPayment = amount / term;
      resultText = `La cuota mensual es: ${calculatedMonthlyPayment.toFixed(
        2
      )} €`;
    } else {
      const calculatedMonthlyPayment =
        (amount * interestRate) / (1 - Math.pow(1 + interestRate, -term));
      resultText = `La cuota mensual es: ${calculatedMonthlyPayment.toFixed(
        2
      )} €`;
    }
  } else if (calculationType === "term") {
    if (isNaN(amount) || isNaN(interestRate) || isNaN(monthlyPayment)) {
      resultText = "Por favor, asegúrese de que todos los valores son válidos.";
    } else {
      let remainingBalance = amount;
      let totalInterest = 0;
      let calculatedTerm = 0;

      while (remainingBalance > 0) {
        let interestPayment = remainingBalance * interestRate;
        totalInterest += interestPayment;
        remainingBalance = remainingBalance + interestPayment - monthlyPayment;
        calculatedTerm++;
        if (calculatedTerm > 1000) {
          // Evitar bucle infinito
          break;
        }
      }

      resultText = `El número de cuotas es: ${calculatedTerm}`;
    }
  } else if (calculationType === "endDate") {
    if (isNaN(amount) || isNaN(interestRate) || isNaN(monthlyPayment)) {
      resultText = "Por favor, asegúrese de que todos los valores son válidos.";
    } else {
      let remainingBalance = amount;
      let totalInterest = 0;
      let calculatedTerm = 0;

      while (remainingBalance > 0) {
        let interestPayment = remainingBalance * interestRate;
        totalInterest += interestPayment;
        remainingBalance = remainingBalance + interestPayment - monthlyPayment;
        calculatedTerm++;
        if (calculatedTerm > 1000) {
          // Evitar bucle infinito
          break;
        }
      }

      const endDate = new Date(startDate);
      endDate.setMonth(startDate.getMonth() + calculatedTerm);
      resultText = `La fecha de finalización es: ${endDate.toLocaleDateString()}`;
    }
  }

  document.getElementById("result").innerText = resultText;
  document.getElementById("specialPaymentSection").style.display = "flex";
}

function calculateAfterSpecialPayment() {
  const amount = parseFloat(document.getElementById("amount").value);
  const interestRate =
    parseFloat(document.getElementById("interestRate").value) / 100 / 12;
  const monthlyPayment = parseFloat(
    document.getElementById("monthlyPayment").value
  );
  const startDate = new Date(document.getElementById("startDate").value);
  const specialPayment = parseFloat(
    document.getElementById("specialPayment").value || 0
  );

  console.log(
    `amount: ${amount}, interestRate: ${interestRate}, monthlyPayment: ${monthlyPayment}, startDate: ${startDate}, specialPayment: ${specialPayment}`
  );

  let remainingBalance = amount;
  let totalInterest = 0;
  let currentDate = new Date();
  let monthsPaid =
    (currentDate.getFullYear() - startDate.getFullYear()) * 12 +
    currentDate.getMonth() -
    startDate.getMonth();

  for (let i = 0; i < monthsPaid; i++) {
    let interestPayment = remainingBalance * interestRate;
    totalInterest += interestPayment;
    remainingBalance = remainingBalance + interestPayment - monthlyPayment;
  }

  if (specialPayment > 0) {
    remainingBalance -= specialPayment;
  }

  console.log(`remainingBalance after specialPayment: ${remainingBalance}`);

  let resultText = "";

  let remainingTerm = 0;

  while (remainingBalance > 0) {
    let interestPayment = remainingBalance * interestRate;
    totalInterest += interestPayment;
    remainingBalance = remainingBalance + interestPayment - monthlyPayment;
    remainingTerm++;
    if (remainingTerm > 1000) {
      // Evitar bucle infinito
      break;
    }
  }

  const newEndDate = new Date(currentDate);
  newEndDate.setMonth(currentDate.getMonth() + remainingTerm);
  newEndDate.setDate(1);
  resultText = `La nueva fecha de finalización es: ${newEndDate.toLocaleDateString()}`;

  document.getElementById("result").innerText = resultText;
}

function goBack() {
  document.getElementById("step1").style.display = "flex";
  document.getElementById("loanForm").style.display = "none";
  document.getElementById("specialPaymentSection").style.display = "none";
  document.getElementById("result").innerText = "";
}

function resetForm() {
  document.getElementById("loanForm").reset();
  document.getElementById("result").innerText = "";
  document.getElementById("specialPaymentSection").style.display = "none";
  document.getElementById("step1").style.display = "flex";
  document.getElementById("loanForm").style.display = "none";
}

document
  .getElementById("toggleDarkMode")
  .addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    document
      .querySelectorAll("input, select, textarea")
      .forEach(function (element) {
        element.classList.toggle("dark-mode");
      });
    document.querySelectorAll("button").forEach(function (element) {
      element.classList.toggle("dark-mode");
    });
  });
