let currentBalance = 0;

async function updateBalance() {
    const response = await fetch('/api/balance');
    const data = await response.json();
    currentBalance = data.balance;
    document.getElementById('balanceValue').textContent = currentBalance.toFixed(2);
}

async function placeBet(choice) {
    const betAmount = parseFloat(document.getElementById('betAmount').value);

    try {
        const response = await fetch('/api/bet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                amount: betAmount,
                choice: choice
            })
        });

        const result = await response.json();

        if(result.error) {
            alert(result.error);
            return;
        }

        document.getElementById('result').innerHTML = `
            🎰 Result: ${result.result.toUpperCase()}<br>
            ${result.win ? '🎉 You won!' : '💥 You lost!'}<br>
            💵 New balance: $${result.new_balance.toFixed(2)}
        `;

        await updateBalance();

    } catch(error) {
        console.error('Error:', error);
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', async () => {
    Telegram.WebApp.ready();
    Telegram.WebApp.expand();
    await updateBalance();
});