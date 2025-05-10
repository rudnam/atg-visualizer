import { notifications } from "@mantine/notifications";

const showError = (title: string, message: string) => {
  notifications.show({
    position: "bottom-center",
    color: "red",
    title,
    message,
  });
};

const showToast = (title: string, message: string) => {
  notifications.show({
    position: "bottom-center",
    title,
    message,
  });
};

export default {
  showToast,
  showError,
};
