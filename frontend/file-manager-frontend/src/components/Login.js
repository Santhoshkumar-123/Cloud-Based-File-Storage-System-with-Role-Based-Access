import React, { useState } from "react";
import axios from "axios";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    try {
      const response = await axios.post(
        "https://cognito-idp.ap-south-1.amazonaws.com/",
        {
          AuthFlow: "USER_PASSWORD_AUTH",
          ClientId: "6dcv1dtvpjm14h1sjur18vsj43",
          AuthParameters: {
            USERNAME: email,
            PASSWORD: password
          }
        },
        {
          headers: {
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target":
              "AWSCognitoIdentityProviderService.InitiateAuth"
          }
        }
      );

      const { IdToken } = response.data.AuthenticationResult;

      // Store IdToken for Cognito Authorizer
      localStorage.setItem("token", IdToken);

      window.location.reload();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.message || "Login failed");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <input
        placeholder="Email"
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={login}>Login</button>
    </div>
  );
};

export default Login;