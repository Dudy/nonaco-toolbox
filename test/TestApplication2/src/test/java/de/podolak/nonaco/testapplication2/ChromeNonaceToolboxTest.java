package de.podolak.nonaco.testapplication2;

import static org.junit.Assert.*;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

/**
 * Unit test for simple App.
 */
public class ChromeNonaceToolboxTest {
    
    private static final Logger LOGGER = Logger.getLogger( ChromeNonaceToolboxTest.class.getName() );

    protected static WebDriver driver;
    protected static String URL = "http://localhost:11080/";
    
    public ChromeNonaceToolboxTest() {
        System.setProperty("java.util.logging.config.file", "resources/logging.properties");
        System.setProperty("webdriver.chrome.driver", "d:\\Code\\Bibliotheken\\Selenium\\chromedriver_v2.2.exe");
    }

    @BeforeClass
    public static void init() {
        driver = new ChromeDriver();
        driver.get(URL);
        getAnchorByText("Login").click();
        getForm().submit();
    }
    
    @AfterClass
    public static void done() {
        driver.close();
    }
    
    protected static void shouldHaveText(String text) {
        try {
            driver.findElement(By.xpath("//*[contains(.,'" + text + "')]"));
            LOGGER.log(Level.FINE, "text ''{0}'' found by xpath", text);
        } catch (NoSuchElementException e) {
            LOGGER.log(Level.SEVERE, "text ''{0}'' not found", text);
            fail("text '" + text + "' not found");
        }
    }
    
    protected static void shouldNotHaveText(String text) {
        try {
            driver.findElement(By.xpath("//*[contains(.,'" + text + "')]"));
            LOGGER.log(Level.SEVERE, "text ''{0}'' found, but not expected", text);
            fail("text '" + text + "' found, but not expected");
        } catch (NoSuchElementException e) {
            LOGGER.log(Level.FINE, "text ''{0}'' not found by xpath (as expected)", text);
        }
    }
    
    protected static void shouldHaveAnchor(String text) {
        try {
            driver.findElement(By.xpath("//a[text()='" + text + "']"));
            LOGGER.log(Level.FINE, "anchor with text ''{0}'' found by xpath", text);
        } catch (NoSuchElementException e) {
            LOGGER.log(Level.SEVERE, "anchor with text ''{0}'' not found", text);
            fail("anchor with text '" + text + "' not found");
        }
    }
    
    protected static WebElement getAnchorByText(String text) {
        WebElement webElement = null;
        
        try {
            webElement = driver.findElement(By.xpath("//a[text()='" + text + "']"));
            LOGGER.log(Level.FINE, "anchor with text ''{0}'' found by xpath", text);
        } catch (NoSuchElementException e) {
            LOGGER.log(Level.SEVERE, "anchor with text ''{0}'' not found", text);
            fail("anchor with text '" + text + "' not found");
        }
        
        return webElement;
    }
    
    /**
     * Returns the first form on the page.
     * 
     * @return form
     */
    protected static WebElement getForm() {
        WebElement webElement = null;
        
        try {
            webElement = driver.findElement(By.xpath("//form"));
            LOGGER.log(Level.FINE, "form found by xpath");
        } catch (NoSuchElementException e) {
            LOGGER.log(Level.SEVERE, "no form found");
            fail("no form found");
        }
        
        return webElement;
    }
    
    protected void checkXPath(WebElement webElement, String xpath) {
        try {
            webElement.findElement(By.xpath(xpath));
            LOGGER.log(Level.FINE, "element found by xpath ''{0}'", xpath);
        } catch (NoSuchElementException e) {
            LOGGER.log(Level.FINE, "element not found by xpath ''{0}'", xpath);
            fail("element not found by xpath '" + xpath + "'");
        }
    }
    
    protected String getHtmlById(String id) {
        WebElement element = driver.findElement(By.id(id));
        String contents = (String)((JavascriptExecutor)driver).executeScript("return arguments[0].innerHTML;", element);
        return contents;
        
//        return driver.findElement(By.id(id)).getAttribute("innerHTML");
    }
    
    protected void assertElementContainsText(String id, String text) {
        assertTrue(getHtmlById(id).contains(text));
    }
}




// jquery stuff
// WebElement element = (WebElement) ((JavascriptExecutor)driver).executeScript("return $('.cheese')[0]");