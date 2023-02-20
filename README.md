<h1 align=center><b>2084</b></h1>

### *The year is 2084...*

Immortality is available to a select few, one of which is Elon Musk (of course). From the result of a Twitter poll, Musk has decided to launch a seige on Earth from his command base on Mars. It is up to you, the final Earth astronaut, to defend Earth from Musk's army of Tesla spaceships. 

---
## Gameplay



The goal is to accumulate as many points as possible. Maybe if you get enough, immortal Elon will call of the seige. Different Telsa spaceships have different point values, weapons, and movements.

| Ship    | Sprite                                                                         | Points | Weapon  | Movement   | Spawn Wave |
| ------- | ------------------------------------------------------------------------------ | ------ | ------- | ---------- | ---------- |
| Proto S | ![Proto S](https://github.com/grant-nations/2084/raw/main/data/orange_04.png)  | 50     | Laser   | Diagonal   | 2          |
| Proto 3 | ![Proto 3](https://github.com/grant-nations/2084/raw/main/data/red_03.png)     | 10     | Laser   | Winding    | 1          |
| Proto X | ![Proto X](https://github.com/grant-nations/2084/raw/main/data/metalic_06.png) | 100    | Missile | Horizontal | 5          |
| Proto Y | ![Proto Y](https://github.com/grant-nations/2084/raw/main/data/green_02.png)   | 80     | Laser   | Sporratic  | 4          |
| Player  | ![Player](https://github.com/grant-nations/2084/raw/main/data/player.png)      |        | Laser   | Horizontal |            |

#### Commands

| Action     | Key        |
| ---------- | ---------- |
| Move left  | `A` or `⇐` |
| Move right | `D` or `⇒` |
| Fire       | `SPACE`    |
| Pause      | `ESC`      |

---
## Setup

#### Linux/MacOS (bash)
---
1. Set up virtual environment (optional)
   
   For example, using [venv](https://docs.python.org/3/library/venv.html): 
   ```
   python venv path/to/twenty84/.venv
   ``` 

2. Activate virtual environment (optional)
   ```
   source path/to/twenty84/.venv/bin/activate
   ```
3. Install [pygame](https://www.pygame.org/news)
   ```
   pip install -r path/to/twenty84/requirements.txt
   ```
4. Launch game
   ```
   python path/to/twenty84/twenty_84.py
   ```
#### Windows
---
1. Set up virtual environment (optional)
   
   For example, using [venv](https://docs.python.org/3/library/venv.html): 
   ```
   python venv path\to\twenty84\.venv
   ``` 

2. Activate virtual environment (optional)

    Using Command Prompt:
   ```
   path\to\twenty84\Scripts\activate.bat
   ```
    Using Powershell:
   ```
   path\to\twenty84\Scripts\Activate.ps1
   ```

3. Install [pygame](https://www.pygame.org/news)
   ```
   pip install -r path\to\twenty84\requirements.txt
   ```
4. Launch game
   ```
   python path\to\twenty84\twenty_84.py
   ```

---
## Artists

- Spaceship sprites: [Dylestorm](https://livingtheindie.itch.io/)
- Space pixel background: [PixelSpace](https://deep-fold.itch.io/)
- Font: [Ænigma](https://www.dafont.com/upheaval.font)