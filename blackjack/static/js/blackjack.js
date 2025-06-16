const dealerHandDiv = document.getElementById('dealer-hand');
const playerHandDiv = document.getElementById('player-hand');
const resultDiv = document.getElementById('result');

const startGameButton = document.getElementById('start-game');
const hitButton = document.getElementById('hit');
const standButton = document.getElementById('stand');

function renderHand(hand, container) {
    container.innerHTML = '';
    const suitSymbols = {
        'Hearts': '♥',
        'Diamonds': '♦',
        'Clubs': '♣',
        'Spades': '♠'
    };
    hand.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card';
        if (card.value === 'hidden') {
            cardDiv.className += ' hidden';
            cardDiv.textContent = '🂠';
        } else {
            const suit = suitSymbols[card.suit] || card.suit;
            const isRed = card.suit === 'Hearts' || card.suit === 'Diamonds';
            if (isRed) cardDiv.classList.add('red');
            cardDiv.innerHTML =
                '<div class="corner tl">' + card.value + '<br>' + suit + '</div>' +
                '<div class="corner br">' + card.value + '<br>' + suit + '</div>' +
                '<div class="center">' + suit + '</div>';
        }
        container.appendChild(cardDiv);
    });
}

startGameButton.addEventListener('click', async () => {
    const response = await fetch('/api/start_game', { method: 'POST' });
    const data = await response.json();
    renderHand(data.dealer_hand, dealerHandDiv);
    renderHand(data.player_hand, playerHandDiv);
    resultDiv.textContent = '';
    startGameButton.disabled = true;
    hitButton.disabled = false;
    standButton.disabled = false;
});

hitButton.addEventListener('click', async () => {
    const response = await fetch('/api/hit', { method: 'POST' });
    const data = await response.json();
    renderHand(data.player_hand, playerHandDiv);
    if (data.result === 'bust') {
        resultDiv.textContent = 'You busted! Dealer wins.';
        hitButton.disabled = true;
        standButton.disabled = true;
        startGameButton.disabled = false;
    }
});

standButton.addEventListener('click', async () => {
    const response = await fetch('/api/stand', { method: 'POST' });
    const data = await response.json();
    renderHand(data.dealer_hand, dealerHandDiv);
    resultDiv.textContent = `${data.result.toUpperCase()}!`;
    hitButton.disabled = true;
    standButton.disabled = true;
    startGameButton.disabled = false;
});