from flask import Flask, render_template, request
import random

app = Flask(__name__)
my_team = 'rcb.png'
ai_team = 'csk.png'
odd_even = 1
choose = 0
runs1 = 0
wickets1 = 3
balls1 = 0
toss_win = 1
runs2 = 0
wickets2 = 3
balls2 = 0


def generate(threshold):
    pbl = []
    n = int(threshold / 1.5)
    for i in range(n, 7):
        if i < threshold:
            pbl.append(i)
        else:
            pbl.extend([i, i])
    return pbl


def batting_first(runs_scored, wickets_remaining, balls_remaining):
    if balls_remaining == 18:
        return random.randint(1, 6)
    rr = runs_scored / (18 - balls_remaining)
    rr = rr - wickets_remaining * 0.25
    if rr >= 3.25:
        pbl = generate(1)
    else:
        pbl = generate(int(6 - rr))
    re = random.choice(pbl)
    if re == 0:
        re = 6
    return re


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/spin', methods=['POST'])
def spin():
    global my_team, ai_team, odd_even
    if request.method == 'POST':
        my_team = request.form['my_team']
        ai_team = request.form['ai_team']
        odd_even = int(request.form['odd_even'])
        return render_template('spin.html', ai_pic=ai_team, my_pic=my_team)


@app.route('/toss', methods=['POST'])
def toss():
    global toss_win, choose
    if request.method == 'POST':
        my_num = int(request.form['my_num'])
        if int(my_num + random.randint(1, 6)) % 2 == 0:
            return render_template('toss.html', ai_pic=ai_team, my_pic=my_team)
        else:
            toss_win = 0
            choose = random.randint(0, 1)
            return render_template('toss1.html', ai_pic=ai_team, my_pic=my_team, runs=runs1, wickets=wickets1)


@app.route('/play1', methods=['POST'])
def play1():
    global choose, runs1, wickets1, balls1
    if request.method == 'POST':
        if balls1 == 0:
            balls1 = balls1 + 1
            return render_template('play1.html', ai_pic=ai_team, my_pic=my_team, runs=runs1, wickets=wickets1,
                                   balls=balls1)
        if toss_win:
            choose = 0
        else:
            choose = 1

        if wickets1 == 0:
            return render_template('next_innings.html', ai_pic=ai_team, my_pic=my_team, runs=runs1 + 1,
                                   wickets=wickets1,
                                   balls=balls1)
        if choose:
            bowl = int(request.form['score'])
            bat = batting_first(runs1, wickets1, (19 - balls1))
        else:
            bat = int(request.form['score'])
            bowl = batting_first(runs1, wickets1, (19 - balls1))
        if bat == bowl:
            wickets1 = wickets1 - 1
            return render_template('wickets.html', ai_pic=ai_team, my_pic=my_team, runs=runs1, wickets=wickets1,
                                   balls=balls1)
        else:
            runs1 = runs1 + bat
            balls1 = balls1 + 1
            return render_template('play1.html', ai_pic=ai_team, my_pic=my_team, runs=runs1, wickets=wickets1,
                                   balls=balls1 - 1)


@app.route('/play2', methods=['POST'])
def play2():
    global runs2, wickets2, balls2
    if request.method == 'POST':
        if balls2 == 0:
            balls2 = balls2 + 1
            return render_template('play2.html', ai_pic=ai_team, my_pic=my_team, runs=runs2, wickets=wickets2,
                                   balls=balls2)
        if wickets2 == 0:
            return render_template('winner.html', ai_pic=ai_team, my_pic=my_team, runs=runs2 + 1,
                                   wickets=wickets2, balls=balls2)
        if choose:
            bowl = int(request.form['score'])
            bat = batting_first(runs1, wickets1, (19 - balls2))
        else:
            bat = int(request.form['score'])
            bowl = batting_first(runs1, wickets1, (19 - balls2))
        if bat == bowl:
            wickets2 = wickets2 - 1
            return render_template('wickets2.html', ai_pic=ai_team, my_pic=my_team, runs=runs2, wickets=wickets2,
                                   balls=balls2)
        else:
            runs2 = runs2 + bat
            balls2 = balls2 + 1
            if runs2 > runs1:
                return
            return render_template('play2.html', ai_pic=ai_team, my_pic=my_team, runs=runs2, wickets=wickets2,
                                   balls=balls2 - 1)


if __name__ == '__main__':
    app.run(debug=True)
