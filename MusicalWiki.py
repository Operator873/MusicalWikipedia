import musicalbeeps
import json
import random
from sseclient import SSEClient as EventSource


def main():
    url = "https://stream.wikimedia.org/v2/stream/recentchange"
    player = musicalbeeps.Player(volume=0.7, mute_output=True)
    notes = ["C", "D", "E", "F", "G", "A", "B", "C5"]
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
                if change['type'] == "edit" and change['wiki'] == "enwiki":
                    old = int(change['length']['old'])
                    new = int(change['length']['new'])
                    diff = old - new
                    if diff >= 1000:
                        player.play_note("C5", .1)
                        print("Edit adding more than 1,000 characters")
                    elif diff < 1000 and diff >= 100:
                        player.play_note("B", .1)
                        print("Edit adding between 100 - 1,000 characters")
                    elif diff < 100 and diff > 0:
                        player.play_note("A", .1)
                        print("Edit adding between 0 and 100 characters")
                    elif diff <= 0 and diff > -100:
                        player.play_note("G", .1)
                        print("Edit removing between 0 and 100 characters")
                    elif diff <= -100 and diff > -1000:
                        player.play_note("F", .1)
                        print("Edit removing 100 - 1,000 characters")
                    elif diff < -1000:
                        player.play_note("E", .1)
                        print("Edit removing more than 1,000 characters.")
                    else:
                        pass
                elif change['type'] == "log" and change['wiki'] == "enwiki":
                    action = str(change['log_type']).upper()
                    if action == "BLOCK":
                        player.play_note("D", .1)
                        print("An account was blocked!")
                    elif action == "NEWUSERS":
                        player.play_note("C", .1)
                        print("A new user created an account!")
                    else:
                        player.play_note(random.choice(notes), .1)
                        print(action + " happened")
            except BaseException:
                pass


print("Enjoy the sound of enwiki")
main()
