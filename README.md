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
| Proto Y | ![Proto Y](https://github.com/grant-nations/2084/raw/main/data/green_02.png)   | 80     | Laser   | Sporadic   | 4          |
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

0. Clone repository

   The folder that 2084 is cloned into will be referred to as `(2084 dir)` in following steps.

   ```
   git clone https://github.com/grant-nations/2084.git (2084 dir)
   ```
   ---
   
1. Create virtual environment <span style="color:cyan">**(OPTIONAL)**</span>
   
   *Note: if this step is skipped, pygame will be installed globally in step 2, but can be uninstalled just as easily with* `pip uninstall pygame`

   For example, using [venv](https://docs.python.org/3/library/venv.html): 


   #### Linux/MacOS (Bash)
   ```
   python -m venv (2084 dir)/.venv
   ```

   ```
   source (2084 dir)/.venv/bin/activate
   ``` 

   #### Windows (Powershell)
   ```
   python -m venv (2084 dir)\.venv
   ```
   ```
   (2084 dir)\Scripts\Activate.ps1
   ``` 

   ---
2. Install [pygame](https://www.pygame.org/news)

   ```
   pip install -r (2084 dir)/requirements.txt
   ```

   ---
3. Launch game
   ```
   python (2084 dir)/twenty_84.py
   ```

---
## Artists

- Spaceship sprites: [Dylestorm](https://livingtheindie.itch.io/)
- Space pixel background: [PixelSpace](https://deep-fold.itch.io/)
- Font: [Ænigma](https://www.dafont.com/upheaval.font)
