const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');
let sessionCode;
let playerName;

export default class Title extends Phaser.Scene {

    // Vars
    handlerScene = false
    sceneStopped = false

    constructor() {
        super({ key: 'title' })
    }

    init(data) {
        sessionCode = data.session_code;
        playerName = data.player_name;
        console.log("Received Data");
        console.log(playerName);
        console.log(sessionCode)
    }

    preload() {
        this.sceneStopped = false
        this.width = this.game.screenBaseSize.width
        this.height = this.game.screenBaseSize.height
        this.handlerScene = this.scene.get('handler')

        let assetRoot = '../assets/';
        this.load.spritesheet('button', assetRoot + 'button.png', { frameWidth: 269, frameHeight: 51 });
        this.load.image("lobbyContainer", assetRoot + "lobbyContainer.png");
    }

    create() {
        const { width, height } = this;
        // CONFIG SCENE         
        this.handlerScene.updateResize(this);
        // CONFIG SCENE 

        // GAME OBJECTS
        this.leaveGameButton = new uiWidgets.TextButton(this, 0, 0, "button", leaveGame, this, 0, 0, 1, 0)
            .setText("Leave Game", {
                fill: "black",
                fontFamily: "Righteous",
                fontSize: '24px', // Scale the font size
                antialias: false
            })
            .eventTextYAdjustment(1);

        this.lobby = new uiWidgets.TextSprite(this, 0, 0, "lobbyContainer")
            .setText("",{
                fill: "black",
                fontFamily: "Righteous",
                fontSize: '40px', // Scale the font size
                antialias: false,
                align: 'center',
                padding: 10
            });

        this.instruction = this.add.text(70,0,"Waiting for host to start the game...",{
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '35px', // Scale the font size
            antialias: false,
            wordWrap: {width: 350},
            align: 'center',
            fixedWidth: 400,
        });

        this.column = new uiWidgets.Column(this, 270, 400);
        this.column.addNode(this.lobby, 0, 464);
        this.column.addNode(this.leaveGameButton, 0, 162);

        // const params = new URLSearchParams(window.location.search);
        // const playerName = params.get('playerName');
        // const sessionCode = params.get('sessionCode');

        console.log('connected');
        socket.emit('join', {
            player_name: playerName,
            session_code: sessionCode
        });
        console.log('request to join');

        socket.on('update_lobby', (players) => {
            console.log('update received');
            console.log(players)
            let text = '';
            players.forEach(player => {
                text += player + '\n';
            })
            this.lobby.text.setText(text);
        });
    }
}
function leaveGame() {
    socket.emit('leave_game', {
        player_name: playerName,
        session_code: sessionCode
    });
    this.sceneStopped = true
    this.scene.stop('title')
    this.handlerScene.cameras.main.setBackgroundColor("#ffffff")
    this.handlerScene.launchScene('login');
    // window.location.href = 'indexOLD.html';

}

window.addEventListener('beforeunload', () => {
    // Emit a leave request when the tab is closed
    socket.emit('leave_game', {
        player_name: playerName,
        session_code: sessionCode
    });
});
