// const params = new URLSearchParams(window.location.search);
// const playerName = params.get('playerName');
// const sessionCode = params.get('sessionCode');
//
//const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');
const socket = io.connect('http://127.0.0.1:5000');

// if (isMobileDevice()) {
//     console.log("in If");
//     gameState.hiddenInputName = document.createElement('inputName');
//     gameState.hiddenInputName.style.position = 'absolute';
//     gameState.hiddenInputName.style.opacity = '0';
//     gameState.hiddenInputName.style.zIndex = '-1';
//     document.body.appendChild(gameState.hiddenInputName);
//
//     gameState.hiddenInputName.addEventListener('inputName', function(event) {
//         gameState.name = event.target.value;
//     });
//
//     gameState.hiddenInputCode = document.createElement('inputCode');
//     gameState.hiddenInputCode.style.position = 'absolute';
//     gameState.hiddenInputCode.style.opacity = '0';
//     gameState.hiddenInputCode.style.zIndex = '-1';
//     document.body.appendChild(gameState.hiddenInputCode);
//
//     gameState.hiddenInputCode.addEventListener('inputCode', function(event) {
//         gameState.code = event.target.value;
//     });
//
// }

let gameState = {}
let maxNameLength = 18;
let maxCodeLength = 6;
let playerName;
let sessionCode;

// gameState.hiddenInputCode = document.createElement('input');
// gameState.hiddenInputCode.style.position = 'absolute';
// gameState.hiddenInputCode.style.opacity = '0';
// gameState.hiddenInputCode.style.zIndex = '-1';
// document.body.appendChild(gameState.hiddenInputCode);
//
// gameState.hiddenInputCode.addEventListener('input', function(event) {
//     gameState.code = event.target.value;
// });

export default class Login extends Phaser.Scene {

    // Vars
    handlerScene = false
    sceneStopped = false

    constructor() {
        super({ key: 'login' })
    }

    preload() {
        gameState = {};

        gameState.hiddenInputName = document.createElement('input');
        gameState.hiddenInputName.style.position = 'absolute';
        gameState.hiddenInputName.style.opacity = '0';
        gameState.hiddenInputName.style.zIndex = '-1';
        document.body.appendChild(gameState.hiddenInputName);

        //inputType insertText
        //deleteContentBackward
        gameState.hiddenInputName.addEventListener('input', function(event) {
            if (gameState.name.length <= maxNameLength) {
                if (event.inputType === 'insertText' && gameState.name.length < maxNameLength) {
                    gameState.name += event.data;
                } else if (event.inputType === 'deleteContentBackward' && gameState.name.length > 0) {
                    gameState.name = gameState.name.slice(0, -1);
                }
            }
        });



        gameState.hiddenInputCode = document.createElement('input');
        gameState.hiddenInputCode.style.position = 'absolute';
        gameState.hiddenInputCode.style.opacity = '0';
        gameState.hiddenInputCode.style.zIndex = '-1';
        document.body.appendChild(gameState.hiddenInputCode);

        gameState.hiddenInputCode.addEventListener('input', function(event) {
            if (gameState.code.length <= maxCodeLength) {
                if (event.inputType === 'insertText' && gameState.code.length < maxCodeLength) {
                    gameState.code += event.data;
                } else if (event.inputType === 'deleteContentBackward' && gameState.code.length > 0) {
                    gameState.code = gameState.code.slice(0, -1);
                }
            }
        });


        this.sceneStopped = false
        this.width = this.game.screenBaseSize.width
        this.height = this.game.screenBaseSize.height
        this.handlerScene = this.scene.get('handler')

        let assetRoot = 'assets/';
        this.load.image("joinContainer", assetRoot + "joinContainer.png");
        this.load.spritesheet('button', assetRoot + 'button.png', { frameWidth: 269, frameHeight: 51 });

    }

    create() {
        const { width, height } = this;
        // CONFIG SCENE
        this.handlerScene.updateResize(this);

        const self = this;
        this.input.keyboard.createCursorKeys();

        this.add.image(269,485, 'joinContainer');
        this.joinGameButton = new uiWidgets.TextButton(this, 0, 0, "button", joinGame, this, 1, 0, 1, 0)
            .setText("Join Game", {
                fill: "black",
                fontFamily: "Righteous",
                fontSize: '24px', // Scale the font size
                antialias: false
            })
            .eventTextYAdjustment(1);

        this.column = new uiWidgets.Column(this, 270, 828);
        this.column.addNode(this.joinGameButton, 0, 0);

        // Initiate form and input field
        const fieldTextConfig = {
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '26px', // Scale the font size
            antialias: false
        };
        //Player name field
        gameState.name = '';
        gameState.nameText = this.add.text(130, 433, gameState.name, fieldTextConfig);
        gameState.isEnteringName = false;

        const nameForm = this.add.graphics({x: 130, y: 433});
        nameForm.fillStyle(0xFFED92, 1).setAlpha(0.2).setDepth(10);
        nameForm.fillRect(0, 0, 300, 42);
        nameForm.setInteractive(new Phaser.Geom.Rectangle(0, 0, 300, 42), Phaser.Geom.Rectangle.Contains);
        activateNameForm(nameForm);

        //Session code field
        gameState.code = '';
        gameState.codeText = this.add.text(130, 586, gameState.code, fieldTextConfig);
        gameState.isEnteringCode = false;

        const codeForm = this.add.graphics({x: 130, y: 586});
        codeForm.fillStyle(0xFFED92, 1).setAlpha(0.2).setDepth(10);
        codeForm.fillRect(0, 0, 300, 42);
        codeForm.setInteractive(new Phaser.Geom.Rectangle(0, 0, 300, 42), Phaser.Geom.Rectangle.Contains);
        activateNameForm(codeForm);


        const cursorConfig = {
            fill: "black",
            fontFamily: "Righteous",
            fontSize: '26px', // Scale the font size
            antialias: false
        };
        gameState.formCursorName = this.add.text(130, 433, '|', cursorConfig);
        gameState.formCursorName.setDepth(21).setAlpha(0);

        gameState.formCursorCode = this.add.text(130, 586, '|', cursorConfig);
        gameState.formCursorCode.setDepth(21).setAlpha(0);

        const cursorTweenName = this.tweens.add({
            targets: gameState.formCursorName,
            alpha: 1,
            duration: 300,
            hold: 600,
            yoyo: true,
            repeat: -1,
            paused: true
        });

        const cursorTweenCode = this.tweens.add({
            targets: gameState.formCursorCode,
            alpha: 1,
            duration: 300,
            hold: 600,
            yoyo: true,
            repeat: -1,
            paused: true
        });


        // Activate/ deactivate the input form
        //NameY :433
        //CodeY: 586
        function activateNameForm (gameObject) {
            gameObject.on('pointerdown', () => {
                switch(gameObject.y){
                    case 433: {
                        if (!gameState.isEnteringName) {
                            gameState.isEnteringName = true;

                            if (gameState.name === '') {
                                gameState.name = '';
                            }
                            gameState.formCursorName.setAlpha(0);
                            cursorTweenName.resume();

                            gameState.hiddenInputName.focus();
                            gameState.hiddenInputCode.blur();
                            self.time.delayedCall(200, () => {
                                deactivateNameForm(gameObject);
                            })
                        }
                        break;
                    }
                    case 586: {
                        if (!gameState.isEnteringCode) {
                            gameState.isEnteringCode = true;

                            if (gameState.code === '') {
                                gameState.code = '';
                            }

                            gameState.formCursorCode.setAlpha(0);
                            cursorTweenCode.resume();

                            gameState.hiddenInputCode.focus();
                            gameState.hiddenInputName.blur();
                            self.time.delayedCall(200, () => {
                                deactivateNameForm(gameObject);
                            })
                        }
                        break;
                    }
                }

            })
        }

        function deactivateNameForm(gameObject) {
            self.input.off('pointerdown');
            self.input.once('pointerdown', () => {
                switch (gameObject.y) {
                    case 433: {
                        if (gameState.isEnteringName) {
                            let delayTime = 0;

                            // Reset form if it's empty
                            if (!gameState.name) {
                                gameState.name = '';
                                delayTime = 100; // Gives Update() time to update the name field before !isEnteringName.
                            }
                            // Deactivates typing
                            self.time.delayedCall(delayTime, () => {
                                gameState.isEnteringName = false;
                            })
                            // Remove cursor
                            gameState.formCursorName.setAlpha(0);
                            cursorTweenName.pause();

                            gameState.hiddenInputName.blur();
                        }
                        break;
                    }
                    case 586: {
                        if (gameState.isEnteringCode) {
                            let delayTime = 0;
                            // Reset form if it's empty
                            if (!gameState.code) {
                                gameState.code = '';
                                delayTime = 100; // Gives Update() time to update the name field before !isEnteringName.
                            }
                            // Deactivates typing
                            self.time.delayedCall(delayTime, () => {
                                gameState.isEnteringCode = false;
                            })
                            // Remove cursor
                            gameState.formCursorCode.setAlpha(0);
                            cursorTweenCode.pause();

                            gameState.hiddenInputCode.blur();
                        }
                        break;
                    }
                }
            });
        }
    }
    update () {
        let textWidth = 0;

        if (gameState.isEnteringName && gameState.name.length <= maxNameLength) {
            // Dynamically updates the displayed input text as it is being typed
            gameState.nameText.setText(gameState.name);
            textWidth = gameState.nameText.width;

            // Dynamically positions the cursor at the end of the typed text
            gameState.formCursorName.x = gameState.nameText.x + textWidth;
        }

        if (gameState.isEnteringCode && gameState.code.length <= maxCodeLength) {
            // Dynamically updates the displayed input text as it is being typed
            gameState.codeText.setText(gameState.code);
            textWidth = gameState.codeText.width;

            // Dynamically positions the cursor at the end of the typed text
            gameState.formCursorCode.x = gameState.codeText.x + textWidth;
        }
    }
}

function joinGame(){
    if (gameState.name.length === 0 || gameState.code.length < 6) {
        //placeholder error text
        console.log("Please enter a valid name or session code");
        return
    }
    playerName = gameState.name;
    sessionCode = gameState.code;

    socket.emit('request_join', {
        player_name: gameState.name,
        session_code: gameState.code
    });

    socket.on('join_approve' + playerName, (player) => {
        let name = player['name'];
        let code = player['code'];

        gameState.nameText.destroy();
        gameState.codeText.destroy();
        gameState.formCursorCode.destroy();
        gameState.formCursorName.destroy();

        gameState.name = '';
        gameState.code = '';

        this.sceneStopped = true;
        this.scene.stop('login');
        this.handlerScene.cameras.main.setBackgroundColor("#ffffff");
        this.handlerScene.launchScene('title', {
            player_name: name,
            session_code: code
        });
    })
}

// Initiate the on-screen keyboard for mobile devices
function isMobileDevice() {
    let value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    console.log(value);
    return value;
}