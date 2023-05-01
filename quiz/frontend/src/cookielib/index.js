import Cookies from "js-cookie";

let exp = {
	getCookieToken: () => {
		return Cookies.get("token");
	},
	setCookieToken: (token) => {
		Cookies.set("token", token, { expires: 365, secure: true });
	},
	removeCookie: () => {
		Cookies.remove("token", { secure: true });
	},
};

export default exp;
