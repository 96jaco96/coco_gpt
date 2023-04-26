# Coco_GPT

## About The Project

A (sort of) simple cli front end for the OpenAI API.

It can "remember" the previous message and user query.\
And you can choose which personality the AI will have.

### Prerequisites


* Python >= 3.9.6

#### NOTE: This was developed using Python 3.9.6, but was tested up to 3.11.2
  

### Installation

1. Get an OpenAI API Key at https://platform.openai.com/account/api-keys


2. Clone and cd in the repo
   ```sh
   git clone https://github.com/96jaco96/coco_gpt.git && cd coco_gpt
   ```
3. Install the requirements
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your API in `config.conf`
   ```
    KEY = PUT YOUR API HERE
   ```
5. Run it!
    ```
    python main.py
    ```
## Usage

The program will give you the available commands when you run it, those commands are:

``` personality ```
to set a new personalityfor the AI\
```clear```
 to forget the previous query, response and personality\
```exit```
 to close the program

## Contributing

    "Your code sucks!" 
                      -cite.

Feel free to contribute then!

Any contributions you make is **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the GPL3 License. See `LICENSE.txt` for more information.
