/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.*;
import java.io.FileNotFoundException;
import java.util.*;
import java.util.logging.Level;
import java.util.logging.Logger;
/**
 * @author weingart
 */
public class Etiquetador {

    /**
     * @param args the command line arguments
     * @throws java.io.FileNotFoundException
     * @throws java.io.UnsupportedEncodingException
     */
    public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException, IOException {
        // TODO code application logic here
        /* Si el argumento que enviamos al programa no es el adecuado, no podemos
         * realizar el etiquetado, por lo cual damos un mensaje de error. */
        if (args.length != 3){
            System.out.println("Error argumentos incorrectos");
            System.exit(0);
	}
        /* Obetenemos la direccion donde se encuentra el archivo */
        String direccion = args[0];
        /* Obtenemos el nombre del archivo a etiquetar */
        String archivo = args[1];
        /* Obtenemos */
        String texto_correcto = args[2];
        /* Pasams a leer el corpus */
        leerCorpus(direccion);
        HashMap< String, HashMap< String, Integer>> corpus2 = parserCorpus("./lexic.txt");
        etiquetarTexto(archivo);
        compararResultados(archivo + "_Etiquetado", texto_correcto);
    }

    static void leerCorpus(String path) {
        String line = "";
        String palabra;
        String categoria;
        int nveces;
        /* Utilizamos el Hashmap debido a su rapido acceso y lo mapeamos de la 
         * siguiente manera [palabra, categoria, nveces]*/
        HashMap< String, HashMap< String, Integer>> corpus = new HashMap<String, HashMap<String, Integer>>();
        try {
            BufferedReader stop = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            /* mientras tengamos lineas por leer */
            while ((line = stop.readLine()) != null) {
                /* Creamos los tokens mediante el split de la linea que estamos
                 * leyendo actualmente. */
                String[] tokens = line.split("\t");
                /* Pasamos a poner las primeras letras que posiblemente puedan
                 * ser mayusculas, en minusculas, de esta manera no diferenciaremos
                 * las palabras que empiecen una oracion de otra que este en medio
                 * de la palabra. ej: Un == un 
                 * Un problema seria palabras como papa y Papa que obviamente tienen
                 * significados diferentes. */
                palabra = tokens[0].toLowerCase();
                /* Cogemos la categoria a la que corresponde la palabra. */
                categoria = tokens[1];
                /* Si el mapa contiene a la palabra... */
                if (corpus.containsKey(palabra)) {
                    HashMap<String, Integer> categoria_existente = corpus.get(palabra);
                    /* Si la palabra posee esa categoria...*/
                    if (categoria_existente.containsKey(categoria)) {
                        /* obtenemos el numero de veces que aparece esa palabra */
                        nveces = categoria_existente.get(categoria);
                        /* y lo aumentamos */
                        ++nveces;
                        /* para volver a guardarlo en el mapa. */
                        categoria_existente.put(categoria, nveces);
                    } else {
                        /* y no posee la categoria, la creamos, y le ponemos el 
                         * calor de 1, ya que es el primero que hemos visto. */
                        categoria_existente.put(categoria, 1);
                    }
                } else {
                    HashMap<String, Integer> categoria_nueva = new HashMap<String, Integer>();
                    categoria_nueva.put(tokens[1], 1);
                    corpus.put(tokens[0], categoria_nueva);
                }
            }
	try {
            escribirCorpus(corpus);
            
        /* Las siguientes lineas se corresponden con los "try and catch" que tenemos
         * en el programa. */
        } catch (UnsupportedEncodingException ex) {
            Logger.getLogger(Etiquetador.class.getName()).log(Level.SEVERE, null, ex);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(Etiquetador.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Etiquetador.class.getName()).log(Level.SEVERE, null, ex);
        }
    } catch (IOException e) { }    
}

    static void etiquetarTexto(String path) throws FileNotFoundException, UnsupportedEncodingException {
        HashMap< String, HashMap<String, Integer>> corpus = parserCorpus("./lexic.txt");
        /* Creamos un File para la version etiquetada. */
        File fichero = new File(path + "_Etiquetado");
        /* Si el fichero existe, lo borramos. */
        if (fichero.exists()) {
            fichero.delete();
        }
        double contador = 0;
        double mas = 0;
        try {
            BufferedWriter Fescribe = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(path + "_Etiquetado", true), "ISO-8859-1"));
            BufferedReader stop = new BufferedReader(new InputStreamReader(new FileInputStream(path), "ISO-8859-1"));
            String line;
            String palabra;
            String palabra2;
            String maximo = "";
            int maxveces = 0;
            int veces;
            String anterior = "";
            while ((line = stop.readLine()) != null) {
                String[] tokens = line.split("\t");
                palabra2 = tokens[0];
                palabra = tokens[0].toLowerCase();

                if (corpus.containsKey(palabra)) {
                    ++contador;
                    HashMap<String, Integer> añadido = corpus.get(palabra);
                    if (añadido.size() > 1) {
                        ++mas;
                    }
                    Iterator it = añadido.entrySet().iterator();
                    maxveces = 0;
                    while (it.hasNext()) {
                        Map.Entry e = (Map.Entry) it.next();
                        veces = (Integer) e.getValue();
                        if (maxveces < veces) {
                            maxveces = veces;
                            maximo = (String) e.getKey();
                        }
                    }
                    anterior = maximo;
                    Fescribe.write(palabra2 + "\t" + maximo + "\r\n");
                } else {
                    if (palabra2.charAt(0) <= 'Z' && palabra2.charAt(0) >= 'A') {
                        Fescribe.write(palabra2 + "\t" + "NP" + "\r\n");
                    } else if (palabra2.charAt(0) <= '9' && palabra2.charAt(0) >= '0') {
                        Fescribe.write(palabra2 + "\t" + "Num" + "\r\n");
                    } else if (anterior.equals("Det")) {
                        Fescribe.write(palabra2 + "\t" + "NC" + "\r\n");
                    } else if (anterior.equals("V")) {
                        Fescribe.write(palabra2 + "\t" + "Prep" + "\r\n");
                    } else if (anterior.equals("Pron")) {
                        Fescribe.write(palabra2 + "\t" + "V" + "\r\n");
                    } else {
                        String corregida = corregir(palabra, corpus);
                        if (corregida == null) {
                            Fescribe.write(palabra2 + "\t" + "V" + "\r\n");
                        } else {
                            ++contador;
                            HashMap<String, Integer> añadido = corpus.get(corregida);
                            if (añadido.size() > 1) {
                                ++mas;
                            }
                            Iterator it = añadido.entrySet().iterator();
                            maxveces = 0;
                            while (it.hasNext()) {
                                Map.Entry e = (Map.Entry) it.next();
                                veces = (Integer) e.getValue();
                                if (maxveces < veces) {
                                    maxveces = veces;
                                    maximo = (String) e.getKey();
                                }
                            }
                            anterior = maximo;
                            Fescribe.write(palabra2 + "\t" + maximo + "\r\n");

                        }
                    }
                }
            }
            System.out.println("Numero de duplicados : " + mas + ". Palabras encontradas en corpus : " + contador);
            Fescribe.close();
        } catch (IOException e) {}
    }

    /* Punto 3 de la practica, en el cual comparamos los datos obtenidos en el
     * test. */
    static double compararResultados(String direccion1, String direccion2) {
        double acertadas = 0;
        double totales = 0;
        double noaparece = 0;
        double fallo = 0;
        try {
            BufferedReader original = new BufferedReader(new InputStreamReader(new FileInputStream(direccion1), "ISO-8859-1"));
            BufferedReader correcto = new BufferedReader(new InputStreamReader(new FileInputStream(direccion2), "ISO-8859-1"));
            String linea_original, linea_correcta;

            while ((linea_original = original.readLine()) != null && (linea_correcta = correcto.readLine()) != null) {
                String[] tokens_original = linea_original.split("\t");
                String[] tokens_correctos = linea_correcta.split("\t");
                if (tokens_original[0].equalsIgnoreCase(tokens_correctos[0]) && tokens_original[1].equals(tokens_correctos[1])) {
                    ++acertadas;
                } else {
                    /*  */
                    if (!tokens1[0].equalsIgnoreCase(tokens2[0]) && tokens1[1].equals(tokens2[1])) {
                        System.out.println("Error \n");
                        System.out.println("Palabra1: " + tokens1[0] + ", Cat : " + tokens1[1] + ". Palabra2: " + tokens2[0] + ", Cat : " + tokens2[1] + "\n");
                    }
                    if (tokens1[1].equals("NOAPARECE")) {
                        ++noaparece;
                    } else {
                        ++fallo;
                    }
                }
                ++totales;
            }

        } catch (IOException e) {
        }
        System.out.println("Acertadas : " + acertadas + ". Totales : " + totales + ". Falladas : " + fallo);
        System.out.println("Porcentaje de acierto : " + (acertadas / totales));
        if (totales != 0) {
            return (acertadas / totales);
        }
        return 0;
    }

    static void escribirCorpus(HashMap< String, HashMap< String, Integer>> corpus) throws UnsupportedEncodingException, FileNotFoundException, IOException {
        File fichero = new File("./lexic.txt");
        /* Si el fichero existe, lo borramos. */
        if (fichero.exists()) {
            fichero.delete();
        }
        try (
            /* Creamos el bufer que se encargara de escribir en el nuevo fichero. */
            BufferedWriter escritor = new BufferedWriter(new OutputStreamWriter(
                    new FileOutputStream("./lexic.txt", true), "utf-8"))) {
            /* Recorremos todas las palabras que tenemos mapeadas. */
            for (Map.Entry palabra : corpus.entrySet()) {
                /* Obtenemos la categoria y sus concurrencias. */
                HashMap<String, Integer> categoria = (HashMap<String, Integer>) palabra.getValue();
                for (Map.Entry e : categoria.entrySet()) {
                    /* Los escribimos segun el patron dado... 
                     * PALABRA\t CATEGORIA\t NVECES\r\n */
                    escritor.write((String) palabra.getKey() + "\t" + (String) e.getKey() + "\t" + (Integer) e.getValue() + "\r\n");
                }
            }
        }
    }

    static HashMap< String, HashMap< String, Integer>> parserCorpus(String direccion) throws FileNotFoundException {
        /* Creamos una tabla de hash */
        HashMap< String, HashMap< String, Integer>> corpus = new HashMap<String, HashMap<String, Integer>>();
        String linea, palabra, categoria;
        int nveces;
        try {
            /* Creamos el bufer de lectura */
            BufferedReader fichero = new BufferedReader(new FileReader(direccion));
            while ((linea = fichero.readLine()) != null) {
                /* Realizamos el split de la linea que estamos viendo. */
                String[] tokens = linea.split("\t");
                /* Cogemos la palabra */
                palabra = tokens[0];
                /* la categoria */
                categoria = tokens[1];
                /* y la concurrencia */
                nveces = Integer.parseInt(tokens[2]);
                /* Si el corpus ya contiene la palabra */
                if (corpus.containsKey(palabra)) {
                    HashMap<String, Integer> actual = corpus.get(palabra);
                    actual.put(categoria, nveces);
                } else {
                    /* sino, lo creamos y la insertamos en el corpus */
                    HashMap<String, Integer> nuevo = new HashMap<String, Integer>();
                    nuevo.put(categoria, nveces);
                    corpus.put(palabra, nuevo);
                }
            }

        } catch (IOException e) {}
        return corpus;
    }

    static String corregir(String word, HashMap< String, HashMap< String, Integer>> corpus) {
        /* Buscamos la palabra */
        Iterator it = corpus.entrySet().iterator();
        while (it.hasNext()) {
            /* Cargamos la tabla */
            Map.Entry tabla = (Map.Entry) it.next();
            String palabra = (String) tabla.getKey();
            boolean encontrado = true;
            /* Vemos si la palabra a corregir es igual a la que tenemos en la tabla, segun su tamaño. */
            if (word.length() == palabra.length()) {
                int i = 0;
                boolean es_diferente = false;
                /* Verificamos que la palabra sea igual que la correcta, caracter
                 * por caracter. */
                while (i < word.length() && encontrado) {
                    if (palabra.charAt(i) != word.charAt(i)) {
                        if (es_diferente) {
                            encontrado = false;
                        } else {
                            es_diferente = true;
                        }
                    }
                    ++i;
                }
                /* Si lo hemos encontrado, devolvemos la palabra. */
                if (encontrado) {
                    return palabra;
                }
            }
        }
        /* Si no hemos encontrado nada, devolvemos un elemento nulo. */
        return null;
    }
}
