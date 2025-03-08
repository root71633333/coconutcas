async function loadProfile() {
    const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getUserProfilePhotos?user_id=${tg.initDataUnsafe.user.id}`);
    const data = await response.json();
    // Отображение аватарки и баланса
}

console.log("Web App initialized!");
tg.enableClosingConfirmation(); // Подтверждение закрытия