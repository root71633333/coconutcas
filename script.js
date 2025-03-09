const BOT_TOKEN = '7546865748:AAE32kq2bPOeUzD84sdTHOYVa4-em0Pz6oQ'; // Ваш токен

document.addEventListener('DOMContentLoaded', () => {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();
    loadUserData();
});

// Загрузка данных пользователя
async function loadUserData() {
    try {
        const tg = window.Telegram.WebApp;
        const userId = tg.initDataUnsafe.user.id;

        // Установка ID пользователя
        document.getElementById('userId').textContent = userId;

        // Загрузка аватарки
        const photosResponse = await fetch(
            `https://api.telegram.org/bot${BOT_TOKEN}/getUserProfilePhotos?user_id=${userId}`
        );
        const photosData = await photosResponse.json();

        if (photosData.result.photos.length > 0) {
            const fileResponse = await fetch(
                `https://api.telegram.org/bot${BOT_TOKEN}/getFile?file_id=${photosData.result.photos[0][0].file_id}`
            );
            const fileData = await fileResponse.json();
            const avatarUrl = `https://api.telegram.org/file/bot${BOT_TOKEN}/${fileData.result.file_path}`;
            document.getElementById('userAvatar').src = avatarUrl;
            document.getElementById('userAvatarLarge').src = avatarUrl;
        }
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
    }
}

// Управление профилем
function toggleProfile() {
    document.getElementById('profilePanel').classList.toggle('active');
}

// Пополнение баланса
function handleDeposit() {
    const tg = window.Telegram.WebApp;
    tg.sendData(JSON.stringify({
        action: 'deposit',
        userId: tg.initDataUnsafe.user.id
    }));
}

// Игровая логика
document.querySelectorAll('.game-card').forEach(card => {
    card.addEventListener('click', () => {
        const game = card.dataset.game;
        document.getElementById(`${game}Game`).classList.add('active');
    });
});

function closeGame() {
    document.querySelector('.coin-game.active').classList.remove('active');
}

function placeBet(side) {
    const betAmount = parseFloat(document.getElementById('betAmount').value);
    const coin = document.getElementById('coin');

    coin.classList.add('flipping');

    setTimeout(() => {
        const tg = window.Telegram.WebApp;
        tg.sendData(JSON.stringify({
            game: 'coinflip',
            bet: betAmount,
            choice: side
        }));
        coin.classList.remove('flipping');
    }, 3000);
}