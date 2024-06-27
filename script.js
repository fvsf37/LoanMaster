// script.js

function calculateCompoundInterest(principal, rate, time) {
  return principal * (1 + rate / 100) ** time - principal;
}

function calculateLoan() {
  // Form validation
  const form = document.getElementById("loan-form");
  if (form.checkValidity() === false) {
    form.classList.add("was-validated");
    return;
  }

  const baseAmount = parseFloat(document.getElementById("base-amount").value);
  const interestRate = parseFloat(
    document.getElementById("interest-rate").value
  );
  const openingFee = parseFloat(document.getElementById("opening-fee").value);
  const installmentValue = parseFloat(
    document.getElementById("installment-value").value
  );
  const startDate = document.getElementById("start-date").value;

  const [day, month, year] = startDate.split("/").map(Number);
  const startDateObj = new Date(year, month - 1, day);

  const currentDate = new Date();
  const monthsPassed =
    (currentDate.getFullYear() - startDateObj.getFullYear()) * 12 +
    (currentDate.getMonth() - startDateObj.getMonth());
  const paidUntilNow = monthsPassed * installmentValue;

  let totalAmount = baseAmount + openingFee;
  if (interestRate > 0) {
    totalAmount += calculateCompoundInterest(baseAmount, interestRate, 1);
  }

  const amortizedCapital = Math.max(
    paidUntilNow -
      calculateCompoundInterest(baseAmount, interestRate, monthsPassed / 12) -
      openingFee,
    0
  );
  let amountRemaining = Math.max(totalAmount - paidUntilNow, 0);

  let totalInstallments = Math.floor(totalAmount / installmentValue);
  let endDate = new Date(startDateObj);
  endDate.setMonth(endDate.getMonth() + totalInstallments);

  document.getElementById(
    "amortized-capital"
  ).textContent = `Capital Amortizado: ${amortizedCapital.toFixed(2)} EUR`;
  document.getElementById(
    "amount-remaining"
  ).textContent = `Cantidad Restante: ${amountRemaining.toFixed(2)} EUR`;
  document.getElementById(
    "end-date"
  ).textContent = `Fecha Estimada de Finalización: ${endDate.toLocaleDateString()}`;

  if (amountRemaining % installmentValue != 0) {
    amountRemaining -= amountRemaining % installmentValue;
    endDate.setMonth(endDate.getMonth() + 1);
  }
}
