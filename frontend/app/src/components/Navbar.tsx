import { Link, useParams } from "react-router-dom";

const Navbar = () => {
  const { accountId } = useParams();

  return (
    <nav>
      <ul>
        <li>
          <Link to={`/accounts/${accountId}/dashboard`}>Dashboard</Link>
        </li>
        <li>
          <Link to={`/accounts/${accountId}/users`}>Users</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
