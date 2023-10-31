//const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');
const socket = io.connect('http://127.0.0.1:5000');

let sessionCode;
let playerName;

export default class Forecast extends Phaser.Scene {

    // Vars
    handlerScene = false
    sceneStopped = false

    constructor() {
        super({ key: 'forecast' })
    }

    init(data) {
        sessionCode = data.session_code;
        playerName = data.player_name;
    }

    preload() {
        this.sceneStopped = false
        this.width = this.game.screenBaseSize.width
        this.height = this.game.screenBaseSize.height
        this.handlerScene = this.scene.get('handler')

        let assetRoot = 'assets/';
        // this.load.spritesheet('button', assetRoot + 'button.png', { frameWidth: 269, frameHeight: 51 });
        // this.load.image("lobbyContainer", assetRoot + "lobbyContainer.png");
    }

    create() {
        const { width, height } = this;
        // CONFIG SCENE
        this.handlerScene.updateResize(this);
        // CONFIG SCENE

        // GAME OBJECTS

        this.instruction = this.add.text(70,80, playerName,{
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '35px', // Scale the font size
            antialias: false,
            wordWrap: {width: 350},
            align: 'center',
            fixedWidth: 400,
        });


        socket.emit('join', {
            player_name: playerName,
            session_code: sessionCode
        });

        socket.on('test_event', (data) => {
            console.log(data);
        });

        //socket.on

    }
}
