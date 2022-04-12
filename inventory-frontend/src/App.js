import { Products } from "./components/Products";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProductsCreate } from "./components/ProductsCreate";
import { Orders } from "./components/Orders";

function App() {
  return <BrowserRouter>
    <Routes>
      <Route path="/" element={<Products />}></Route>
      <Route path="/create" element={<ProductsCreate />}></Route>

      {/* Orders can be created on different microservice */}
      <Route path="/orders" element={<Orders />}></Route> 

    </Routes>
  </BrowserRouter>;
}

export default App;
