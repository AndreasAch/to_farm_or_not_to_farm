// const params = new URLSearchParams(window.location.search);
// const playerName = params.get('playerName');
// const sessionCode = params.get('sessionCode');
//

let gameState = {}
const socket = io.connect('https://to-farm-or-not-tofarm.onrender.com');

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

gameState.hiddenInputName = document.createElement('input');
gameState.hiddenInputName.style.position = 'absolute';
gameState.hiddenInputName.style.opacity = '0';
gameState.hiddenInputName.style.zIndex = '-1';
document.body.appendChild(gameState.hiddenInputName);

gameState.hiddenInputName.addEventListener('input', function(event) {
    gameState.name = event.target.value;
});

gameState.hiddenInputCode = document.createElement('input');
gameState.hiddenInputCode.style.position = 'absolute';
gameState.hiddenInputCode.style.opacity = '0';
gameState.hiddenInputCode.style.zIndex = '-1';
document.body.appendChild(gameState.hiddenInputCode);

gameState.hiddenInputCode.addEventListener('input', function(event) {
    gameState.code = event.target.value;
});

export default class Login extends Phaser.Scene {

    // Vars
    handlerScene = false
    sceneStopped = false

    constructor() {
        super({ key: 'login' })
    }

    preload() {
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
        this.joinGameButton = new uiWidgets.TextButton(this, 0, 0, "button", joinGame, this, 0, 0, 1, 0)
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

                            if (isMobileDevice()) {
                                gameState.hiddenInputName.focus();
                            }

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

                            if (isMobileDevice()) {
                                gameState.hiddenInputCode.focus();
                                console.log("Should focus");
                            }

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
                            // Deactivate the on-screen keyboard for mobile devices
                            if (isMobileDevice()) {
                                gameState.hiddenInputName.blur();
                            }
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
                            // Deactivate the on-screen keyboard for mobile devices
                            if (isMobileDevice()) {
                                gameState.hiddenInputCode.blur();
                            }
                        }
                        break;
                    }
                }
            });
        }

        // Log key strokes if isEnteringName === true
        this.input.keyboard.on('keydown', (event) => {
            if (gameState.isEnteringName) {
                // Cap the name length to keep the text from overflowing the form
                const maxNameLength = 18
                // Implement backspace
                if (event.keyCode === 8 && gameState.name.length > 0) {
                    gameState.name = gameState.name.slice(0, -1);

                    // Add any other characters you want to allow
                } else if (event.key.length === 1 && event.key.match(/[a-zA-Z0-9\s\-_]/) && gameState.name.length < maxNameLength) {
                    gameState.name += event.key;

                    // Gently informs the player that its time to stop typing
                } else if (gameState.name.length === maxNameLength) {
                    self.cameras.main.shake(30, .0010, false);
                }
            }

            if (gameState.isEnteringCode) {
                const maxCodeLength = 6
                // Implement backspace
                if (event.keyCode === 8 && gameState.code.length > 0) {
                    gameState.code = gameState.code.slice(0, -1);

                    // Add any other characters you want to allow
                } else if (event.key.length === 1 && event.key.match(/[a-zA-Z0-9\s\-_]/) && gameState.code.length < maxCodeLength) {
                    gameState.code += event.key;

                    // Gently informs the player that its time to stop typing
                } else if (gameState.code.length === maxCodeLength) {
                    self.cameras.main.shake(30, .0010, false);
                }
            }
        });

        function startgame() {
            if (gameState.name === 'Enter your name...' || gameState.name === '') {
                gameState.name = 'Punk Rock Samurai'; // Set your own default name
            }

            console.log(`Name: ${gameState.name}`);

            // Replace with your code to start the game
            self.cameras.main.fadeOut(1000);
            self.cameras.main.shake(1000, .0030, false);
        }

        // Updates the button sprite in response to pointerover/ pointerout events
        function animateButton(button) {
            button.on('pointerover', function () {
                this.setTexture('rectangularButtonHovered');
            });

            button.on('pointerout', function () {
                this.setTexture('rectangularButton');
            });
        }

    }
    update () {
        let textWidth = 0;

        if (gameState.isEnteringName) {
            // Dynamically updates the displayed input text as it is being typed
            gameState.nameText.setText(gameState.name);
            textWidth = gameState.nameText.width;

            // Dynamically positions the cursor at the end of the typed text
            gameState.formCursorName.x = gameState.nameText.x + textWidth;
        }

        if (gameState.isEnteringCode) {
            // Dynamically updates the displayed input text as it is being typed
            gameState.codeText.setText(gameState.code);
            textWidth = gameState.codeText.width;

            // Dynamically positions the cursor at the end of the typed text
            gameState.formCursorCode.x = gameState.codeText.x + textWidth;
        }
    }
}

function joinGame(){
    socket.emit('join_game', {
        player_name: gameState.name,
        session_code: gameState.code
    });

    this.sceneStopped = true
    this.scene.stop('login')
    this.handlerScene.cameras.main.setBackgroundColor("#ffffff")
    this.handlerScene.launchScene('title', {
        player_name: gameState.name,
        session_code: gameState.code
    });
}

// Initiate the on-screen keyboard for mobile devices
function isMobileDevice() {
    let value = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    console.log(value);
    return value;
}