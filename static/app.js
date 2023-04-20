const BASE_URL = 'http://127.0.0.1:5000/api';

// ?given data about a cupcake, create the HTML

function generateCupcakeHTML(cupcake) {
  return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
          <button class="delete-button">X</button>
        </li>
        <img class="Cupcake-img"
              src="${cupcake.image}"
              alt="(no image provided)">
      </div>
    `;
}

//? Put initial cupcakes on page

async function showCupcakes() {
  response = await axios.get(`${BASE_URL}/cupcakes`);
  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $('#cupcakes').append(newCupcake);
  }
}

// ? ON FORM SUBMIT PREVENT PAGE REFRESH, GRAB FORM VALUES, POST TO DB, CREATE HTML, APPEND TO DOM, RESET FORM
$('#new-cupcake').on('submit', async function (event) {
  event.preventDefault();

  let flavor = $('#form-flavor').val();
  let rating = $('#form-rating').val();
  let size = $('#form-size').val();
  let image = $('#form-image').val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, { flavor, rating, size, image });

  let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));

  $('#cupcakes').append(newCupcake);
  $('#new-cupcake').trigger('reset');
});

// ? DELETE BUTTON, ON CLICK, PREVENT PAGE REFRESH, SELECT CORRECT ELEMENT, GET ID, MAKE DELETE REQUEST TO DB, REMOVE FROM DOM
$('#cupcakes').on('click', '.delete-button', async function (event) {
  event.preventDefault();
  let $cupcake = $(event.target).closest('div');
  let cupcakeId = $cupcake.attr('data-cupcake-id');

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});
// ? RUN THE SHOW ALL CUPCAKES WHEN DOM LOADS /IS LOADED
$(showCupcakes);
