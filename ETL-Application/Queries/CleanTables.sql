UPDATE politician SET fullname = "Chuck Grassley" WHERE fullname = "ChuckGrassley";
UPDATE politician SET fullname = "Dan Sullivan" WHERE fullname = "sendansullivan";

UPDATE politician SET fullname = REPLACE(fullname, "Archive: ", "") WHERE fullname LIKE "%Archive: %";
UPDATE politician SET fullname = REPLACE(fullname, ", M.D.", "") WHERE fullname LIKE "%, M.D.";
UPDATE politician SET fullname = REPLACE(fullname, "U.S. ", "") WHERE fullname LIKE "%U.S. %";
UPDATE politician SET fullname = REPLACE(fullname, "Senator ", "") WHERE fullname LIKE "%Senator %";
UPDATE politician SET fullname = REPLACE(fullname, "Sen. ", "") WHERE fullname LIKE "%Sen. %";
UPDATE politician SET fullname = REPLACE(fullname, "Sen ", "") WHERE fullname LIKE "%Sen %";
