import { playerName } from '../../main.js';
import { sessionCode } from '../../main.js';
import { gameStarted } from "../../main.js";

export default class Preload extends Phaser.Scene {

    width = null
    height = null
    handlerScene = null
    sceneStopped = false

    constructor() {
        super({ key: 'preload' })
    }

    preload() {
        // Images
        this.load.image('guide', 'assets/images/540x960-guide.png')

        //---------------------------------------------------------------------->
        this.canvasWidth = this.sys.game.canvas.width
        this.canvasHeight = this.sys.game.canvas.height

        this.width = this.game.screenBaseSize.width
        this.height = this.game.screenBaseSize.height

        this.handlerScene = this.scene.get('handler')
        this.handlerScene.sceneRunning = 'preload'
        this.sceneStopped = false


        this.load.on('complete', () => {
            this.time.addEvent({
                callback: () => {
                    this.sceneStopped = true
                    this.scene.stop('preload')
                    this.handlerScene.cameras.main.setBackgroundColor("#ffffff")
                    console.log(gameStarted);
                    if (gameStarted === 'true') {
                        console.log('forecast');
                        this.handlerScene.launchScene('forecast', {player_name: playerName, session_code: sessionCode, game_started: gameStarted});
                    } else {
                        console.log('title');
                        this.handlerScene.launchScene('title', {player_name: playerName, session_code: sessionCode, game_started: gameStarted});
                    }
                    //this.handlerScene.launchScene('title', {player_name: playerName, session_code: sessionCode, game_started: gameStarted});

                },
                loop: false
            })
        })
    }

    create() {
        const { width, height } = this
        // CONFIG SCENE         
        this.handlerScene.updateResize(this)
        // CONFIG SCENE 

        // GAME OBJECTS  

        // GAME OBJECTS  
    }
}
