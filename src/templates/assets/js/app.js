import React from "react";
import ReactDOM from "react-dom";
import CreateProduct from "./components/CreateProduct";
import EditProduct from "./components/EditProduct";

// require('./bootstrap');
// require('./sb-admin');

function isEditProductPage() {
  return window.location.pathname.includes("product/edit");
}

const propsContainer = document.getElementById("variants");
const props = Object.assign({}, propsContainer.dataset);

// const propsContainer_edit = document.getElementById("variants_edit");
// const props_edit = Object.assign({}, propsContainer_edit.dataset);

// ReactDOM.render(
//     <React.StrictMode>
//         <CreateProduct {...props}/>
//     </React.StrictMode>,
//     document.getElementById('root')
// );
ReactDOM.render(
  <React.StrictMode>
    {isEditProductPage() ? (
      <EditProduct {...props} />
    ) : (
      <CreateProduct {...props} />
    )}
  </React.StrictMode>,
  document.getElementById("root")
);
