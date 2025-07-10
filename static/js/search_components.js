const head = document.head || document.getElementsByTagName("head")[0];

let filterContent = []

function submitFilter() {

  let filterData = {
    "brand": [],
    "wear": [],
    "color": [],
    "maxPrice": 0,
    "year": 0
  }
  
  let brandSelection = $('.brands-selection');
  let wearSelection = $('.wear-selection');
  let colorSelection = $('.color-selection');
  
  for (let i = 0; i < brandSelection.length; i++) {
    if (brandSelection[i].checked) {
      filterData['brand'].push(brandSelection[i].value)
    }
  }
  for (let i = 0; i < wearSelection.length; i++) {
    if (wearSelection[i].checked) {
      filterData['wear'].push(wearSelection[i].value)
    }
  }
  for (let i = 0; i < colorSelection.length; i++) {
    if (colorSelection[i].checked) {
      filterData['color'].push(colorSelection[i].value)
    }
  }
  filterData['maxPrice'] = $("#range1")[0].value
  filterData['year'] = parseInt($("#year-select")[0].value)
  if (filterData['year'] == "Select year") {
    return;
  }
  $.post("/working", JSON.stringify(filterData), (data, status) => {
    filterContent = JSON.parse(data);
    root.render(<App />);
  });
}

function App() {
  let filterItems = []
  console.log(filterContent)
  for (let i = 0; i < filterContent.length; i++) {
    filterItems.push(
      <a href={`/car/${filterContent[i]['id']}`} key={i}>
        <div className={"car rounded-4 shadow"}>
          <img src={`/static/imgs/${filterContent[i]['filename']}`}></img>
          <div className = {"info"}>
            <h1>{`${filterContent[i]['brand']} ${filterContent[i]['model']}`}</h1>
            <p>Year: {filterContent[i]['year']}</p>
            <h2>$ {filterContent[i]['price']}</h2>
          </div>
        </div>
      </a>
    )
  }
  return (<div>{filterContent.length > 0 && filterItems}</div>)
}

const root = ReactDOM.createRoot(document.querySelector("#root"));
root.render(<App />);