const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');
//const socket = io.connect('http://127.0.0.1:5000');

// // Check if the Wake Lock API is available in the browser
// if ('wakeLock' in navigator) {
//     // Request a screen wake lock
//     async function requestWakeLock() {
//         try {
//             const wakeLock = await navigator.wakeLock.request('screen')
//             console.log('Screen wake lock activated:', wakeLock)
//         } catch (err) {
//             console.error('Failed to request a wake lock:', err)
//         }
//     }
//
//     // Request the wake lock when the page is focused
//     document.addEventListener('visibilitychange', () => {
//         if (document.visibilityState === 'visible') {
//             requestWakeLock()
//         }
//     })
// } else {
//     console.error('Wake Lock API is not supported in this browser.')
// }

let sessionCode;
let playerName;
let playerClass;

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
        playerClass = data.player_class;
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

        this.player_name = this.add.text(70,80, playerName,{
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '35px', // Scale the font size
            antialias: false,
            wordWrap: {width: 350},
            align: 'center',
            fixedWidth: 400,
        });

        this.player_class = this.add.text(70,130, playerClass,{
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '35px', // Scale the font size
            antialias: false,
            wordWrap: {width: 350},
            align: 'center',
            fixedWidth: 400,
        });

        this.round_text = this.add.text(70,180, "Round: 0",{
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '35px', // Scale the font size
            antialias: false,
            wordWrap: {width: 350},
            align: 'center',
            fixedWidth: 400,
        });

        this.forecast = this.add.text(100,380, "",{
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '28px', // Scale the font size
            antialias: false,
            align: 'center',
        });


        socket.emit('join', {
            player_name: playerName,
            session_code: sessionCode
        });

        socket.on('distribute_forecast' + playerName, (data) => {
            console.log(data);
            this.forecast.setText(
                "FORECAST:" + "\n" +
                "Upcoming round: " + data[0] + " 55%" + "\n" +
                "Round+1: " + data[1] + " 45%" + "\n" +
                "Round+2: " + data[2] + " 35%" + "\n"
            )
        });

        socket.on('advance_client_round', (round) => {
            this.forecast.setText("");
            this.round_text.setText("Round: " + round);
        });

        //socket.on

    }
}


