const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');
//const socket = io.connect('http://127.0.0.1:5000');
import {Sprite} from './sprite.js';

// Check if the Wake Lock API is available in the browser
if ('wakeLock' in navigator) {
    // Request a screen wake lock
    async function requestWakeLock() {
        try {
            const wakeLock = await navigator.wakeLock.request('screen')
            console.log('Screen wake lock activated:', wakeLock)
            this.scene.stop('title');
            this.handlerScene.cameras.main.setBackgroundColor("#ffffff")
            this.handlerScene.launchScene('forecast', {
                player_name: playerName,
                session_code: sessionCode,
                player_class: playerClass[0]
            });
        } catch (err) {
            console.error('Failed to request a wake lock:', err)
        }
    }

    // Request the wake lock when the page is focused
    document.addEventListener('visibilitychange', () => {
        // if (document.visibilityState === 'visible') {
        //     requestWakeLock()
        // }
        requestWakeLock()
    })
} else {
    console.error('Wake Lock API is not supported in this browser.')
}


let sessionCode;
let playerName;
let playerClass;
let round_num;

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
        socket.emit('request_round');
    }

    preload() {
        this.sceneStopped = false
        this.width = this.game.screenBaseSize.width
        this.height = this.game.screenBaseSize.height
        this.handlerScene = this.scene.get('handler')

        let assetRoot = 'assets/';
        this.load.image("forecast_name_label", assetRoot + "forecast_name_label.png");
        this.load.image("forecast_upcoming", assetRoot + "forecast_upcoming.png");
        this.load.image("forecast_next", assetRoot + "forecast_next.png");
        this.load.image("forecast_label", assetRoot + "forecast_label.png");
        this.load.image("forecast_after_next", assetRoot + "forecast_after_next.png");
        this.load.image("round_label", assetRoot + "round_label.png");
        this.load.image("Normal", assetRoot + "normal128.png");
        this.load.image("Drought", assetRoot + "drought128.png");
        this.load.image("Rain", assetRoot + "rain128.png");
        this.load.image("Hail", assetRoot + "hail128.png");
    }

    create() {
        const { width, height } = this;
        // CONFIG SCENE
        this.handlerScene.updateResize(this);
        // CONFIG SCENE

        this.round_text = new uiWidgets.TextSprite(this, 0, 0, "round_label")
            .setText("Round 0", {
                fill: "black",
                fontFamily: "Righteous",
                fontSize: '25px', // Scale the font size
                antialias: false,
                align: 'center',
            })
        this.add.container(275,42, this.round_text)

        // GAME OBJECTS
        // this.player_name_container = new Container(this, 270, 115, [this.player_name, new text])
        this.player_name = new uiWidgets.TextSprite(this, 0, 0, "forecast_name_label")
            .setText(playerName,{
                fill: "black",
                fontFamily: "Righteous",
                fontSize: '23px', // Scale the font size
                antialias: false,
                align: 'center',
            });
        this.add.container(270,115, this.player_name)

        let font_family_title = {
            fill: "#780202",
            fontFamily: "Righteous",
            fontSize: '22px', // Scale the font size
            antialias: false,
            align: 'center',
            fontWeight: '600pt'
        }

        let font_family_text = {
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '20px', // Scale the font size
            antialias: false,
            align: 'center',
        }

        this.upcoming_round = new uiWidgets.TextSprite(this, 270, 301, "forecast_upcoming");
        this.next_round = new uiWidgets.TextSprite(this, 270, 560, "forecast_next");
        this.after_next_round = new uiWidgets.TextSprite(this, 270, 819, "forecast_after_next");

        this.upcoming_event = new uiWidgets.TextSprite(this, 153, 310);
        this.title_upcoming = new uiWidgets.TextSprite(this, 0, 0, "forecast_label").setText("", font_family_title);
        this.add.container(369,265, this.title_upcoming);
        this.text_upcoming = new uiWidgets.TextSprite(this, 0, 0, "forecast_label").setText("", font_family_text);
        this.add.container(369,351, this.text_upcoming);

        this.next_event = new uiWidgets.TextSprite(this, 153, 569);
        this.title_next = new uiWidgets.TextSprite(this, 0, 0, "forecast_label").setText("", font_family_title);
        this.add.container(369,524,  this.title_next);
        this.text_next = new uiWidgets.TextSprite(this, 0, 0, "forecast_label").setText("", font_family_text);
        this.add.container(369,610, this.text_next);

        this.after_next_event = new uiWidgets.TextSprite(this, 153, 824);
        this.title_after_next = new uiWidgets.TextSprite(this, 0, 0, "forecast_label").setText("", font_family_title);
        this.add.container(369,787,  this.title_after_next);
        this.text_after_next = new uiWidgets.TextSprite(this, 0, 0, "forecast_label").setText("", font_family_text);
        this.add.container(369,873,  this.text_after_next);


        socket.emit('join', {
            player_name: playerName,
            session_code: sessionCode
        });

        socket.on('clear_forecast', () => {
            this.title_upcoming.setText("", font_family_title);
            this.upcoming_event.sprite.destroy();
            this.text_upcoming.setText("", font_family_text);

            this.title_next.setText("", font_family_title)
            this.next_event.sprite.destroy();
            this.text_next.setText("", font_family_text);

            this.title_after_next.setText("", font_family_title)
            this.after_next_event.sprite.destroy();
            this.text_after_next.setText("", font_family_text);
        });

        socket.on('distribute_forecast' + playerName, (data) => {
            console.log(data)
            for (let i in data) {
                switch (i) {
                    case '0': {
                        console.log(i);
                        console.log(data[i]);
                        this.title_upcoming.setText(data[i], font_family_title);
                        this.upcoming_event.sprite = new Sprite(this, 153, 310, data[i]);
                        this.upcoming_event.setVisible(true);
                        this.text_upcoming.setText("With a 85% chance", font_family_text);
                        //this.upcoming_event.sprite(data[i]);
                        break;
                    }
                    case '1': {
                        this.title_next.setText(data[i], font_family_title)
                        this.next_event.sprite = new Sprite(this, 153, 569, data[i]);
                        this.next_event.setVisible(true);
                        this.text_next.setText("With a 70% chance", font_family_text);
                        break;
                    }
                    case '2': {
                        this.title_after_next.setText(data[i], font_family_title)
                        this.after_next_event.sprite = new Sprite(this, 153, 824, data[i]);
                        this.after_next_event.setVisible(true);
                        this.text_after_next.setText("With a 55% chance", font_family_text);
                        break;
                    }
                }
            }
        });

        socket.on('advance_client_round', (round) => {
            this.round_text.setText("Round " + round, {
                fill: "black",
                fontFamily: "Righteous",
                fontSize: '25px', // Scale the font size
                antialias: false,
                align: 'center',
            });
            this.title_upcoming.setText("", font_family_title);
            this.upcoming_event.sprite.destroy();
            this.text_upcoming.setText("", font_family_text);

            this.title_next.setText("", font_family_title)
            this.next_event.sprite.destroy();
            this.text_next.setText("", font_family_text);

            this.title_after_next.setText("", font_family_title)
            this.after_next_event.sprite.destroy();
            this.text_after_next.setText("", font_family_text);
        });

        //socket.on

    }
}
