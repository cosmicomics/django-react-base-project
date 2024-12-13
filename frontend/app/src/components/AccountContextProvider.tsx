import { createContext, useContext, ReactNode } from "react";

const AccountContext = createContext<{ accountId?: string }>({
  accountId: undefined,
});

export const useAccountContext = () => useContext(AccountContext);

export const AccountContextProvider = ({
  children,
  accountId,
}: {
  children: ReactNode;
  accountId?: string;
}) => {
  return (
    <AccountContext.Provider value={{ accountId }}>
      {children}
    </AccountContext.Provider>
  );
};
