// view full entries
class Entry extends React.Component {
  render() {
  return (
    <div>
      <div className = "every-entry">
        <h5>{this.props.date} {this.props.mood}</h5>
        <p>I am grateful for {this.props.grateful}</p>
        <p>I resolve to {this.props.resolution}</p>
        <p>I affirm that {this.props.affirmation}</p>
        <p>I am proud that {this.props.proud}</p>
        <p>I am excited to {this.props.excited}</p>
        <p>I will self-care by {this.props.self_care}</p>
        <p>{this.props.jam}</p>
        <p>{this.props.whine}</p>
      </div>
    </div>
  );
  }
}

function displayEntry() {
class EntryContainer extends React.Component {
  constructor() {
    super();

    this.state = { entries: [] };  // Set initial value
    this.updateDates = this.updateDates.bind(this);
  }

  updateDates(response) {
    const entries = response.entries;
    this.setState({ entries: entries });
  }

  getAllDates() {
    $.get('/api/entries', this.updateDates);
  }

  componentDidMount() {
    this.getAllDates();
  }

  render() {
    const entries = [];
    for (const currentEntry of this.state.entries) {
      //conditional goes here
      entries.push(
        <Entry
          key={currentEntry.entry_id}
          date={currentEntry.date}
          mood={currentEntry.mood}
          grateful={currentEntry.grateful}
          resolution={currentEntry.resolution}
          affirmation={currentEntry.affirmation}
          proud={currentEntry.proud}
          excited={currentEntry.excited}
          self_care={currentEntry.self_care}
          jam={currentEntry.jam}
          whine={currentEntry.whine}
        />
      );
    }

    return (
      <div>
        <div>{entries}</div>
      </div>
    );
  }
}

function displayToday() {
class TodayContainer extends React.Component {
  constructor() {
    super();

    this.state = { entries: [] };  // Set initial value
    this.updateDates = this.updateDates.bind(this);
  }

  updateDates(response) {
    const entries = response.entries;
    this.setState({ entries: entries });
  }

  getAllDates() {
    $.get('/api/today_entry', this.updateDates);
  }

  componentDidMount() {
    this.getAllDates();
  }

  render() {
    const entries = [];
    for (const currentEntry of this.state.entries) {
      //conditional goes here
      entries.push(
        <Entry
          key={currentEntry.entry_id}
          date={currentEntry.date}
          mood={currentEntry.mood}
          grateful={currentEntry.grateful}
          resolution={currentEntry.resolution}
          affirmation={currentEntry.affirmation}
          proud={currentEntry.proud}
          excited={currentEntry.excited}
          self_care={currentEntry.self_care}
          jam={currentEntry.jam}
          whine={currentEntry.whine}
        />
      );
    }

    return (
      <div>
        <div>{entries}</div>
      </div>
    );
  }
}

// Render Today
ReactDOM.render(<TodayContainer />, document.getElementById('entry')
);
}

const showToday = (
  <button onClick={displayToday}>View Today</button>
);

ReactDOM.render(showToday, document.getElementById('showToday'));




// Render View All
ReactDOM.render(<EntryContainer />, document.getElementById('entry')
);
}

const showAll = (
  <button onClick={displayEntry}>View All</button>
);

ReactDOM.render(showAll, document.getElementById('showAll'));



