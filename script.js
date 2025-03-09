const tg = window.Telegram.WebApp;
let balance = 100.00;

// Инициализация
tg.ready();
tg.expand();

// Загрузка профиля
document.getElementById('userPhoto').src = tg.initDataUnsafe.user.photo_url;
document.getElementById('userId').textContent = `ID: ${tg.initDataUnsafe.user.id}`;

// Обновление баланса
function updateBalance() {
    document.getElementById('balanceValue').textContent = balance.toFixed(2);
}

// Открытие игры
document.querySelectorAll('.game-card').forEach(card => {
    card.addEventListener('click', () => {
        const game = card.dataset.game;
        openGame(game);
    });
});

function openGame(game) {
    document.getElementById(`${game}Game`).classList.add('active');
}

function closeGame() {
    document.querySelector('.coin-container.active').classList.remove('active');
}

// Логика Coin Flip
function placeBet(side) {
    const betAmount = parseFloat(document.getElementById('betAmount').value);
    if (betAmount > balance) {
        alert('Not enough balance!');
        return;
    }

    const coin = document.getElementById('coin');
    coin.classList.add('flipping');

    setTimeout(() => {
        const result = Math.random() > 0.5 ? 'heads' : 'tails';
        coin.classList.remove('flipping');

        if (result === side) {
            balance += betAmount;
            alert(`You won $${betAmount}!`);
        } else {
            balance -= betAmount;
            alert(`You lost $${betAmount}!`);
        }

        updateBalance();
        tg.sendData(JSON.stringify({
            game: 'coinflip',
            bet: betAmount,
            choice: side,
            result: result,
            balance: balance
        }));
    }, 3000);
}

updateBalance();