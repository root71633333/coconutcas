const BOT_TOKEN = '7546865748:AAE32kq2bPOeUzD84sdTHOYVa4-em0Pz6oQ';

document.addEventListener('DOMContentLoaded', () => {
    tg.ready();
    tg.expand();
    loadProfile();
});

async function loadProfile() {
    try {
        const userId = tg.initDataUnsafe.user.id;
        const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getUserProfilePhotos?user_id=${userId}`);
        const data = await response.json();

        if(data.result.photos.length > 0) {
            const fileResponse = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getFile?file_id=${data.result.photos[0][0].file_id}`);
            const fileData = await fileResponse.json();
            document.getElementById('userAvatar').src = `https://api.telegram.org/file/bot${BOT_TOKEN}/${fileData.result.file_path}`;
        }
    } catch (e) {
        console.error('Error loading profile:', e);
    }
}

// Подтверждение перед закрытием
tg.enableClosingConfirmation();