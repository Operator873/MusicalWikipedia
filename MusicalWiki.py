import musicalbeeps
import json
from sseclient import SSEClient as EventSource


def main():
    url = "https://stream.wikimedia.org/v2/stream/recentchange"
    player = musicalbeeps.Player(volume=0.5, mute_output=True)
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
                if change['type'] == "edit" and change['wiki'] == "enwiki":
                    old = int(change['length']['old'])
                    new = int(change['length']['new'])
                    diff = old - new
                    if diff >= 1000:
                        player.play_note("C5", .3)
                        print("Edit adding more than 1,000 characters")
                    elif diff < 1000 and diff >= 10:
                        player.play_note("B", .3)
                        print("Edit adding between 10 - 1,000 characters")
                    elif diff < 10 and diff > 0:
                        player.play_note("A", .3)
                        print("Edit adding between 0 and 10 characters")
                    elif diff <= 0 and diff > -10:
                        player.play_note("G", .3)
                        print("Edit removing between 0 and 10 characters")
                    elif diff <= -10 and diff > -1000:
                        player.play_note("F", .3)
                        print("Edit removing 10 - 1,000 characters")
                    elif diff < -1000:
                        player.play_note("E", .3)
                        print("Edit removing more than 1,000 characters.")
                    else:
                        pass
                elif change['type'] == "log" and change['wiki'] == "enwiki":
                    action = str(change['log_type']).upper()
                    if action == "BLOCK":
                        player.play_note("D", .3)
                        print("An account was blocked!")
                    elif action == "NEWUSER":
                        player.play_note("C", .3)
                        print("A new user created an account!")
                    else:
                        play.play_note("C3", .3)
                        print("Some other log action happened")
            except BaseException:
                pass


print("Enjoy the sound of enwiki")
main()
