document.addEventListener("DOMContentLoaded", () => {
  const blocks = document.querySelectorAll(".block");
  const game = setupGame("x", blocks);
  document.querySelector("#current-player").innerHTML = "x";

  for (const [blockIndex, block] of blocks.entries()) {
    block.onclick = blockClickFunction(blockIndex, game); // 1
  }
});

const blockClickFunction = (blockIndex, game) => async () => {
  if (!game().gameOver) {
    game().markBlock(blockIndex);
    await game().aiMove();
  }
  updateUi(game);
};

const setupGame = (startingPlayer, blocks) => {
  let gameObject = {
    currentPlayer: startingPlayer,
    gameOver: false,
    board: [null, null, null, null, null, null, null, null, null], // 2
    blocks,
    markBlock,
    checkForWinner,
    togglePlayer,
    playerWon,
    aiMove,
  };
  // 3
  return () => gameObject;
};

// 4
function markBlock(index) {
  if (!this.gameOver && !this.board[index]) {
    this.blocks[index].classList.add(this.currentPlayer);

    this.board[index] = this.currentPlayer;
    this.togglePlayer();
  }
  this.checkForWinner();
}

function checkForWinner() {
  const WIN_CONDITIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  // Complete the checkForWinner funciton using the WIN_CONDITIONS provided above
  // Try and use native array methods :)
  for (const el of WIN_CONDITIONS) {
    const [x, y, z] = el;

    if (
      this.board[x] &&
      this.board[y] === this.board[x] &&
      this.board[z] === this.board[x]
    ) {
      this.playerWon(this.currentPlayer);
      return this.currentPlayer;
    }
  }
}

function togglePlayer() {
  if (this.currentPlayer === "x") {
    this.currentPlayer = "o";
  } else {
    this.currentPlayer = "x";
  }
}

function playerWon(player) {
  this.togglePlayer();
  this.winningPlayer = player;
  this.gameOver = true;
}

// 5
async function aiMove() {
  if (!this.gameOver) {
    let payload = {
      board: this.board,
      isGameOver: this.gameOver,
    };
    const res = await fetch("http://127.0.0.1:5000/", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    const move = await res.text();
    this.markBlock(parseInt(move));
  }
}

const updateUi = (game) => {
  if (!game().gameOver) {
    document.querySelector("#current-player").innerHTML = game().currentPlayer;
  } else {
    document.querySelector("#current-player-state").innerHTML = `Player ${
      game().currentPlayer
    } won!`;
  }
};
