import { Outlet, useParams } from "react-router-dom";
import Navbar from "./components/Navbar";
import { AccountContextProvider } from "./components/AccountContextProvider";

const App = () => {
  const { accountId } = useParams();

  return (
    <AccountContextProvider accountId={accountId}>
      <Navbar />
      <Outlet />
    </AccountContextProvider>
  );
};

export default App;
