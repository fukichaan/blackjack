from flask import Flask, render_template, jsonify, session, request
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッション管理用

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def create_deck():
    return [{'suit': suit, 'value': value} for suit in SUITS for value in VALUES]

def card_value(card):
    if card['value'] in ['J', 'Q', 'K']:
        return 10
    if card['value'] == 'A':
        return 11
    return int(card['value'])

def hand_value(hand):
    value = sum(card_value(card) for card in hand)
    # Aを1として数え直す
    aces = sum(1 for card in hand if card['value'] == 'A')
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def deal_card(deck):
    return deck.pop()

@app.route('/')
def index():
    return render_template('blackjack.html')

@app.route('/api/start_game', methods=['POST'])
def start_game():
    deck = create_deck()
    random.shuffle(deck)
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    session['deck'] = deck
    session['player_hand'] = player_hand
    session['dealer_hand'] = dealer_hand
    # ディーラーの2枚目は隠す
    dealer_hand_for_client = [dealer_hand[0], {'suit': '', 'value': 'hidden'}]
    return jsonify({
        'player_hand': player_hand,
        'dealer_hand': dealer_hand_for_client
    })

@app.route('/api/hit', methods=['POST'])
def hit():
    deck = session['deck']
    player_hand = session['player_hand']
    player_hand.append(deal_card(deck))
    session['deck'] = deck
    session['player_hand'] = player_hand
    if hand_value(player_hand) > 21:
        return jsonify({'player_hand': player_hand, 'result': 'bust'})
    return jsonify({'player_hand': player_hand, 'result': 'continue'})

@app.route('/api/stand', methods=['POST'])
def stand():
    deck = session['deck']
    player_hand = session['player_hand']
    dealer_hand = session['dealer_hand']
    # ディーラーの2枚目を公開
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
    player_score = hand_value(player_hand)
    dealer_score = hand_value(dealer_hand)
    if dealer_score > 21 or player_score > dealer_score:
        result = 'win'
    elif player_score < dealer_score:
        result = 'lose'
    else:
        result = 'draw'
    return jsonify({
        'dealer_hand': dealer_hand,
        'result': result
    })

if __name__ == '__main__':
    app.run(debug=True)