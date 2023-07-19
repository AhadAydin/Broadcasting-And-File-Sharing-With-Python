# UDP Broadcasting for Chunk Names

This Python script utilizes UDP broadcasting to send and receive messages containing chunk names between computers on the same network. The script broadcasts the names of the chunks it has and listens for messages from other computers to store their chunk names in a dictionary. It also allows the user to input a chunk name and checks if there is a matching chunk name received from other computers and downloads the chunk.

## Usage

1. Ensure that all computers are connected to the same local network.
2. Run the Python script on each computer that will participate in the UDP broadcasting.
3. The script will start broadcasting the names of the chunks it has and listen for incoming messages.
4. When receiving a message from another computer, the script will store the chunk names in a dictionary.
5. To check if a specific chunk name exists in the received chunks from other computers, input the chunk name when prompted.
6. The script will search the dictionary for a matching chunk name and display the result.

## File Description

- `udp_broadcast.py`: The main Python script that handles the UDP broadcasting and receiving logic. It sends and receives UDP messages containing chunk names and stores them in a dictionary.
- `README.md`: This file, providing information about the UDP Broadcasting project.

## Dependencies

This project requires the `socket` module in Python, which is a built-in module for handling networking operations.

## Contributions

Contributions to this project are welcome. If you have any suggestions, bug reports, or improvements, feel free to open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to modify and adapt this README file to suit your needs. Include any additional information or instructions specific to your UDP Broadcasting project. Enjoy broadcasting and receiving chunk names across computers on your local network!
 
