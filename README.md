<div align="center">

# ByteBlast

**A BlockBlast clone and solver in PyGame**

<img src="docs/images/preview.gif" alt="Demo" width="300" />

</div>

## About

ByteBlast is a
[BlockBlast](https://play.google.com/store/apps/details?id=com.block.juggle)
clone using [PyGame](https://www.pygame.org/) that includes an auto solver that
uses a backtracking algorithm to find solutions. BlockBlast is a puzzle game
where players place blocks on a grid to clear rows and columns much like Tetris.

### Features

- **Block movement and placement**: use the keyboard keys to move and place
  blocks on the grid.
- **Line clear**: clear entire rows and columns when they are filled.
- **Random solvable block generation**: generates new blocks that can always be
  solved.
- **Score tracking**: track the users score as they place blocks and clear
  lines.
- **Auto-solve**: an algorithm that automatically solves the puzzle indefinitely
  using backtracking.

## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/andrianllmm/byteblast.git
   cd byteblast
   ```
2. Create and activate a virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate for Windows
   ```
3. Install the dependencies
   ```sh
   pip install -r requirements.txt
   ```
4. Start the game
   ```sh
   python src/main.py
   ```

## Contributing

Contributions are welcome! To get started:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## Issues

Found a bug or issue? Report it on the
[issues page](https://github.com/andrianllmm/byteblast/issues).
