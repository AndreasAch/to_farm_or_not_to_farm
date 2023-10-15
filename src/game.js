const params = new URLSearchParams(window.location.search);
const playerName = params.get('playerName');
const sessionCode = params.get('sessionCode');

const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');

const config = {
    type: Phaser.AUTO,
    height: '100%',
    parent: 'gameWrapper',
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    scale: {
        mode: Phaser.Scale.RESIZE,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 360,
        height: 800
    },
    backgroundColor: '#ffff9f',
    antialias: false,
    render: {
        pixelArt: true
    },
};

const game = new Phaser.Game(config);
// const gameWidth = game.sys.game.canvas.width
// const gameHeight = game.sys.game.canvas.height
// console.log(gameWidth, gameHeight);

let textStyle = {
    'fill': 'black',
    'fontFamily': 'Righteous',
    'fontSize': '24px',
    antialias: false
};

function preload() {
    socket.emit('join', {
        player_name: playerName,
        session_code: sessionCode
    });

    let assetRoot = '/to_farm_or_not_to_farm/assets/';
    this.load.spritesheet('button', assetRoot + 'button.png', { frameWidth: 204, frameHeight: 39 });
    this.load.image("lobbyContainer", assetRoot + "lobbyContainer.png");
}

function create() {
    // Create your game objects and initialize game state
    let leaveGameButton = new uiWidgets.TextButton(this, 0, 0, "button", leaveGame, this, 0, 0, 1, 0)
        .setText("Leave Game", textStyle)
        .eventTextYAdjustment(1);

    let lobby = new uiWidgets.TextSprite(this, 38, 163, "lobbyContainer").setText('', textStyle).setOrigin(0.0, 0.0);

    // var buttonTwo = new uiWidgets.TextButton(this, 0, 0, "button", continueCallback, this, 1, 0, 2, 1)
    //     .setText("Continue", textStyle)
    //     .eventTextYAdjustment(3);
    // var buttonThree = new uiWidgets.TextButton(this, 0, 0, "button", optionsCallback, this, 1, 0, 2, 1)
    //     .setText("Options", textStyle)
    //     .eventTextYAdjustment(3);

    let column = new uiWidgets.Column(this, 0, 0);
    column.addNode(lobby, paddingX=0, paddingY=0);
    column.addNode(leaveGameButton, paddingX=182, paddingY=515);
    // column.addNode(buttonTwo, paddingX=0, paddingY=10);
    // column.addNode(buttonThree, paddingX=0, paddingY=10);

    socket.on('update_lobby', (players) => {
        // const playerList = document.getElementById('playerList');
        // playerList.innerHTML = '';
        // players.forEach(player => {
        //     const listItem = document.createElement('li');
        //     listItem.textContent = player;
        //     playerList.appendChild(listItem);
        // });
        let text = '';
        players.forEach(player => {
            text += player + '\n';
        })
        this.header.text.setText(text);
    });
}

function update() {
}


function leaveGame() {
    socket.emit('leave_game', {
        player_name: playerName,
        session_code: sessionCode
    });

    window.location.href = 'index.html';
}

window.addEventListener('beforeunload', () => {
    // Emit a leave request when the tab is closed
    socket.emit('leave_game', {
        player_name: playerName,
        session_code: sessionCode
    });
});