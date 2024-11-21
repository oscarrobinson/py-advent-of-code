# py-advent-of-code

Repo for Python solutions for Advent of Code past and present


## Setup

The start.sh script builds files for a day. It fetches the input from the AoC site. You'll need to add your session cookie to a file in the root directory named `.aoc.cookie`.

Then to start a problem, build the files by providing the year and the day:

```shell
./start 2023 2
```

The input for the day will be auto copied into the `input.txt` folder.

Update the `test_input.txt` with the test input provided in the challenge and update the test assertions with the provided answer.

Run the tests:
```shell
./test 2023 2
```

Once you think you have a working solution, run to get the final result:
```shell
./run 2023 2
```
